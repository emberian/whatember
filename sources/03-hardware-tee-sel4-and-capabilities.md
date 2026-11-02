# Hardware Roots of Trust, Multi-Vendor TEE Attestation, Confidential GPU E2EE, Bare-Metal `seL4` Microkit, & Post-Quantum Object-Capability Security

> **Primary-Source Technical Dossier**  
> **Scope:** `breadstuffs` (`tee-verify`, `tee-produce`, `cell::tee_attest`, `dregg-chutes-e2ee`, `attest-check`, `sel4/`, `grain-jail`, `macaroon`, `token`, `dregg-auth`, `dregg-pq`, `pqvrf`, `credentials`, `intent`, `audit`, `starbridge-apps`), `degg-research` (`experiments/shielded-baseline`), `nanodregg` (`sandbox`), and `~/elide/breadstuffs` (`95e87c6f`).

---

## 1. Multi-Vendor Hardware TEE Quote Verifier & Enclave Producer (`tee-verify`, `tee-produce`, `cell::tee_attest`)

### 1.1 Substrate Integration (`dregg-cell::tee_attest`)

Inside the cell layer ([`cell/src/tee_attest.rs`](file:///Users/ember/dev/breadstuffs/cell/src/tee_attest.rs#L1-L320)), hardware TEE attestation is integrated as a canonical `WitnessedPredicateKind::Custom` verifier keyed by the domain-separated verification key [`tee_predicate_vk()`](file:///Users/ember/dev/breadstuffs/cell/src/tee_attest.rs#L65-L68):

```rust
pub const TEE_ATTEST_DOMAIN: &[u8] = b"dregg-tee-attestation-verifier-v1";

pub fn tee_predicate_vk() -> [u8; 32] {
    canonical_predicate_vk(TEE_ATTEST_DOMAIN)
}
```

Quotes from all supported hardware vendors share a 1-byte discriminant prefix ([`TeeQuoteKind`](file:///Users/ember/dev/breadstuffs/cell/src/tee_attest.rs#L74-L105)) followed by the vendor-native attestation payload ([`encode_tee_proof`](file:///Users/ember/dev/breadstuffs/cell/src/tee_attest.rs#L222-L227), [`decode_tee_proof`](file:///Users/ember/dev/breadstuffs/cell/src/tee_attest.rs#L230-L237)):

```rust
#[derive(Clone, Copy, Debug, PartialEq, Eq, Serialize, Deserialize)]
#[repr(u8)]
pub enum TeeQuoteKind {
    SevSnp = 1,
    IntelTdx = 2,
    IntelSgx = 3,
    AwsNitro = 4,
}
```

TCB evaluation across platforms is normalized into [`TcbStatus`](file:///Users/ember/dev/breadstuffs/cell/src/tee_attest.rs#L118-L169) and [`TeeReportClaims`](file:///Users/ember/dev/breadstuffs/cell/src/tee_attest.rs#L174-L185):

```rust
#[derive(Clone, Copy, Debug, PartialEq, Eq, Serialize, Deserialize)]
pub enum TcbStatus {
    /// Platform exposes a TCB version and it meets the verifier's pinned minimum.
    MetPolicy,
    /// Platform exposes a TCB version and it falls below the verifier's pinned minimum.
    BelowPolicy,
    /// Platform's attestation document carries NO TCB-version rung (e.g. AWS Nitro).
    NoPolicyOnPlatform,
}

#[derive(Clone, Debug, PartialEq, Eq, Serialize, Deserialize)]
pub struct TeeReportClaims {
    /// 32-byte enclave image measurement (`MRENCLAVE`, `MRTD`, `MEASUREMENT`, or folded `PCR0..2`).
    pub measurement: [u8; 32],
    /// 32-byte user-supplied `report_data` bound into the hardware signature.
    pub report_data: [u8; 32],
    /// Platform TCB status relative to the verifier's pinned policy.
    pub tcb: TcbStatus,
}
```

`TcbStatus::as_token()` emits wire strings `"met-pinned-minimum"`, `"below-pinned-minimum"`, and `"no-tcb-rung-on-this-platform"`; [`TcbStatus::is_refusal()`](file:///Users/ember/dev/breadstuffs/cell/src/tee_attest.rs#L141-L144) returns `true` iff `matches!(self, Self::BelowPolicy)`.

The cell-layer predicate adapter [`TeeWitnessedPredicateVerifier`](file:///Users/ember/dev/breadstuffs/cell/src/tee_attest.rs#L199-L319) is fail-closed by default (`inner: Option<Arc<dyn TeeAttestationVerifier>>` is `None` in [`TeeWitnessedPredicateVerifier::fail_closed()`](file:///Users/ember/dev/breadstuffs/cell/src/tee_attest.rs#L207-L209)). When a concrete verifier is installed, [`TeeWitnessedPredicateVerifier::verify`](file:///Users/ember/dev/breadstuffs/cell/src/tee_attest.rs#L246-L319) enforces four conditions:
1. Decodes `(kind, report_bytes)` via `decode_tee_proof(proof_bytes)`.
2. Calls `verifier.verify_report(kind, report_bytes)` to validate the hardware vendor's cryptographic signature chain.
3. Checks `&claims.measurement == commitment` (the cell's `StateConstraint::Witnessed` 32-byte commitment must equal the enclave's code measurement).
4. Checks `claims.report_data == Self::input_commitment(input)?` (where `PredicateInput::FieldElement(v)` from `grain_turn::ATTESTATION_SLOT` is SHA-256 hashed via `Sha256::digest(b"dregg-tee-field-input-v1:" || v.to_le_bytes())` or passed raw as `PredicateInput::Bytes32`) and `!claims.tcb.is_refusal()`.

---

### 1.2 AWS Nitro Enclaves (`NitroVerifier`)

Implemented in [`tee-verify/src/lib.rs`](file:///Users/ember/dev/breadstuffs/tee-verify/src/lib.rs#L101-L361) (introduced in commit `17b6e5539`, 2026-07-11, hardened in commit `a9d5df4db`, 2026-09-30), [`NitroVerifier`](file:///Users/ember/dev/breadstuffs/tee-verify/src/lib.rs#L121-L216) verifies AWS Nitro Hypervisor attestation documents without any external network calls:

- **Pinned Hardware Root of Trust**: [`AWS_NITRO_ROOT_PEM`](file:///Users/ember/dev/breadstuffs/tee-verify/src/lib.rs#L94-L95) embeds [`tee-verify/src/aws_nitro_root_g1.pem`](file:///Users/ember/dev/breadstuffs/tee-verify/src/aws_nitro_root_g1.pem) (`CN=aws.nitro-enclaves, O=Amazon, C=US`, valid `2019-10-28T13:22:05Z` to `2049-10-28T14:22:05Z`, P-384 public key, SHA-256 fingerprint `641a0321a3e244efe456463195d606317ed7cdcc3c1756e09893f3c68f79bb5b`).
- **CBOR `COSE_Sign1` & `AttDoc` Parsing**:
  - [`CoseSign1`](file:///Users/ember/dev/breadstuffs/tee-verify/src/lib.rs#L102-L103) is deserialized via `ciborium` as a 4-tuple `(ByteBuf, ciborium::Value, ByteBuf, ByteBuf)` representing `[protected, unprotected, payload, signature]`, optionally wrapped in CBOR tag `18`. The signature length must be exactly `96` bytes (`r || s`, 48 bytes each for P-384).
  - [`AttDoc`](file:///Users/ember/dev/breadstuffs/tee-verify/src/lib.rs#L106-L118) is deserialized from `payload`:
    ```rust
    struct AttDoc {
        module_id: String,
        digest: String,
        timestamp: u64,
        pcrs: BTreeMap<u8, ByteBuf>,
        certificate: ByteBuf,
        cabundle: Vec<ByteBuf>,
        #[serde(default)]
        public_key: Option<ByteBuf>,
        #[serde(default)]
        user_data: Option<ByteBuf>,
        #[serde(default)]
        nonce: Option<ByteBuf>,
    }
    ```
  - Requires `!doc.module_id.is_empty()` and `doc.digest == "SHA384"`.
- **X.509 Certificate Chain Verification ([`verify_cert_chain`](file:///Users/ember/dev/breadstuffs/tee-verify/src/lib.rs#L247-L284))**:
  1. Parses `pinned_root_der` from `AWS_NITRO_ROOT_PEM` and asserts `doc.cabundle[0].as_slice() == pinned_root_der.contents.as_slice()` (byte-exact root match).
  2. Constructs the full chain `[cabundle[0], cabundle[1..], certificate]` and parses every DER certificate via `x509-parser`.
  3. Checks X.509 validity windows (`cert.validity().is_valid_at(t)`) at `ref_time = doc.timestamp / 1000` (converting Nitro's millisecond timestamp to Unix seconds).
  4. Verifies every parent→child link `window[1].verify_signature(Some(window[0].public_key()))`.
- **ES384 `COSE_Sign1` Signature Verification ([`verify_cose_sig`](file:///Users/ember/dev/breadstuffs/tee-verify/src/lib.rs#L288-L315))**:
  - Serializes RFC 8152 §4.4 `Sig_structure = ["Signature1", protected, b"", payload]` to CBOR bytes.
  - Extracts the leaf certificate's P-384 SEC1 public key (`p384::ecdsa::VerifyingKey::from_sec1_bytes`) and verifies the 96-byte ECDSA-P384/SHA-384 signature (`p384::ecdsa::Signature::from_slice(sig_bytes)`).
- **Measurement Folding & `report_data` Extraction**:
  - [`fold_pcrs`](file:///Users/ember/dev/breadstuffs/tee-verify/src/lib.rs#L321-L341) verifies that `PCR0` (enclave image), `PCR1` (Linux kernel + bootstrap), and `PCR2` (application) are each present and 48 bytes (SHA-384), then folds them into a 32-byte commitment:
    $$\text{measurement} = \text{SHA-256}(\text{PCR}_0 \mathbin{\Vert} \text{PCR}_1 \mathbin{\Vert} \text{PCR}_2)$$
  - [`extract_report_data`](file:///Users/ember/dev/breadstuffs/tee-verify/src/lib.rs#L345-L361) requires `doc.user_data` to be `Some` and at least 32 bytes; if `doc.user_data` is 32 bytes it copies it directly into `claims.report_data` (rejecting documents with missing `user_data` so an empty `user_data` can never collide with `[0u8; 32]`).
  - Sets `claims.tcb = TcbStatus::NoPolicyOnPlatform` because Nitro attestation documents do not expose a numeric TCB SPL vector.
- **Document Freshness Enforcement ([`check_nitro_freshness`](file:///Users/ember/dev/breadstuffs/tee-verify/src/lib.rs#L182-L202))**:
  - Added in commit `a9d5df4db` to close audit finding **F10**: fails closed if `now_secs == 0`, if `doc.timestamp == 0`, if `doc_ts > now_secs + MAX_FUTURE_SKEW_SECS` (`60` seconds), or if `now_secs - doc_ts > max_age_secs` (default [`MAX_DOC_AGE_SECS = 3600`](file:///Users/ember/dev/breadstuffs/tee-verify/src/lib.rs#L140)).

---

### 1.3 AMD SEV-SNP (`SnpVerifier`)

Implemented in [`tee-verify/src/snp.rs`](file:///Users/ember/dev/breadstuffs/tee-verify/src/snp.rs#L1-L650) and [`tee-verify/src/snp_chain.rs`](file:///Users/ember/dev/breadstuffs/tee-verify/src/snp_chain.rs#L1-L406) (introduced in commit `8ce36ba16`, 2026-07-11; RSA-PSS ARK/ASK chain added in `261a06f8d`, 2026-07-13; policy/VMPL/corroboration/CRL gates added in `4d98292c2` and `3bf5e041a`, 2026-09-30), `SnpVerifier` validates AMD SEV-SNP hardware attestation reports:

#### Fixed Binary Layout (`ATTESTATION_REPORT`, 1184 bytes = `0x4A0`)
Per AMD Publication #56860 (SEV-SNP ABI Specification, Table 22), [`SnpAttestationReport::parse`](file:///Users/ember/dev/breadstuffs/tee-verify/src/snp.rs#L218-L299) parses the exact little-endian offsets ([`snp.rs:69-81`](file:///Users/ember/dev/breadstuffs/tee-verify/src/snp.rs#L69-L81)):

| Constant | Byte Offset | Size | Field & Verification Rule |
|---|---|---|---|
| `OFF_VERSION` | `0x000` | 4B (`u32`) | Report format version; must be `2` or `3` (`MIN_REPORT_VERSION = 2`, `MAX_REPORT_VERSION = 3`) |
| `OFF_GUEST_SVN` | `0x004` | 4B (`u32`) | Guest Security Version Number; checked against `SnpPolicy::min_guest_svn` |
| `OFF_POLICY` | `0x008` | 8B (`u64`) | Guest `POLICY` bitfield (Table 9: bit 16 `SMT`, bit 17 `RESERVED_MBO`, bit 18 `MIGRATE_MA`, bit 19 `DEBUG`, bit 20 `SINGLE_SOCKET`) |
| `OFF_VMPL` | `0x030` | 4B (`u32`) | Virtual Machine Privilege Level (`0..=3`); must be `0` under default policy |
| `OFF_SIGNATURE_ALGO` | `0x034` | 4B (`u32`) | Must equal `SIG_ALGO_ECDSA_P384_SHA384 = 1` |
| `OFF_CURRENT_TCB` | `0x038` | 8B (`u64`) | Current platform `TCB_VERSION` |
| `OFF_KEY_INFO` | `0x048` | 4B (`u32`) | Bits `[4:2]` (`SIGNING_KEY` = `(key_info >> 2) & 0b111`) must equal `SIGNING_KEY_VCEK = 0` (VLEK `1` rejected) |
| `OFF_REPORT_DATA` | `0x050` | 64B | Guest-supplied `REPORT_DATA`; `report_data_32()` extracts `[0x050..0x070]` |
| `OFF_MEASUREMENT` | `0x090` | 48B | 384-bit launch digest (`MEASUREMENT`); `folded_measurement()` computes `SHA-256(measurement)` |
| `OFF_HOST_DATA` | `0x0C0` | 32B | Hypervisor-supplied `HOST_DATA` |
| `OFF_REPORTED_TCB` | `0x180` | 8B (`u64`) | `REPORTED_TCB` bound into the VCEK certificate extensions |
| `OFF_CHIP_ID` | `0x1A0` | 64B | Unique 512-bit processor `CHIP_ID` |
| `OFF_SIGNATURE` | `0x2A0` | 512B | ECDSA P-384 signature over `&raw[..0x2A0]`: `R` at `0x2A0..0x2E8` (72B LE), `S` at `0x2E8..0x330` (72B LE) |

In [`verify_snp_signature`](file:///Users/ember/dev/breadstuffs/tee-verify/src/snp.rs#L334-L361), the verifier checks that the upper 24 padding bytes (`[48..72]`) of both 72-byte little-endian `R` and `S` buffers are all zero, reverses the lower 48 bytes (`[..48]`) of each from little-endian to big-endian SEC1 scalar order, constructs `p384::ecdsa::Signature::from_scalars(r_be, s_be)`, and verifies `&raw_report[..0x2A0]` (`SIGNED_BODY_LEN = 672` bytes) using ECDSA-P384 with SHA-384.

#### Processor Generation TCB Layout (`TcbVersion`)
[`TcbVersion`](file:///Users/ember/dev/breadstuffs/tee-verify/src/snp.rs#L105-L185) handles both the legacy Milan/Genoa 8-byte layout and the Turin 8-byte layout:
- **Milan / Genoa (`from_le_u64`)**: `b[0] = bootloader`, `b[1] = tee`, `b[2..6] = reserved`, `b[6] = snp`, `b[7] = microcode` (`fmc = 0`).
- **Turin (`from_le_u64_turin`)**: `b[0] = fmc`, `b[1] = bootloader`, `b[2] = tee`, `b[3] = snp`, `b[4..7] = reserved`, `b[7] = microcode`.
- [`TcbVersion::meets(&self, floor: &Self)`](file:///Users/ember/dev/breadstuffs/tee-verify/src/snp.rs#L166-L172) enforces component-wise dominance:
  ```rust
  self.fmc >= floor.fmc
      && self.bootloader >= floor.bootloader
      && self.tee >= floor.tee
      && self.snp >= floor.snp
      && self.microcode >= floor.microcode
  ```

#### ARK → ASK → VCEK Certificate Chain & X.509 OIDs (`snp_chain.rs`)
[`tee-verify/src/snp_chain.rs`](file:///Users/ember/dev/breadstuffs/tee-verify/src/snp_chain.rs#L48-L183) embeds the DER-encoded AMD Root Key (ARK) and AMD SEV Signing Key (ASK) bundles fetched from `https://kdsintf.amd.com/vcek/v1/{Product}/cert_chain` on 2026-07-13 for all three EPYC generations ([`SnpProduct`](file:///Users/ember/dev/breadstuffs/tee-verify/src/snp_chain.rs#L65-L98)):

| Product | Family/Model | Pinned ARK SHA-256 | Pinned ASK SHA-256 |
|---|---|---|---|
| **Milan** (Zen 3) | Family `19h`, Model `00h–0Fh` | `69D063B45344D26A2E94E1F4210DE49EF555308287D4C174445C95639A540BCD` | `767B409B0DC90F5D7F2E2CE3E63D0C8B84E8A3122A557D5D56D3B1B6A82C4C38` |
| **Genoa** (Zen 4) | Family `19h`, Model `10h–1Fh` / `A0h–AFh` | `4C6598D19C18719C5DFD4A7D335F674E5BFE1D8F800CEA2CF270C10D103DB2F1` | `84B8F522B5B9A77C779A2C8C60C90F6623082917D981E5A9786E9244D4D34394` |
| **Turin** (Zen 5) | Family `1Ah`, Model `00h–1Fh` | `1F084161A44BB6D93778A904877D4819CAFA5D05EF4193B2DED9DD9C73DD3F6A` | `94C13A3B3F9B7B2B1B6877F9E9C69F63922416C7476645F3F1B84F0F7F4D5D0F` |

[`verify_vcek_against_amd_root`](file:///Users/ember/dev/breadstuffs/tee-verify/src/snp_chain.rs#L223-L320) executes a 5-stage verification:
1. **ARK Self-Signature**: Verifies `SHA256(ark_der) == product.ark_sha256()` and checks the ARK self-signature via [`verify_rsassa_pss_sha384`](file:///Users/ember/dev/breadstuffs/tee-verify/src/snp_chain.rs#L329-L361) (OID `1.2.840.113549.1.1.10`, RSA-4096 PSS with SHA-384 digest, MGF1-SHA-384, 48-byte salt via `rsa::pss::VerifyingKey::<Sha384>`).
2. **ASK ← ARK Signature**: Asserts `ask.issuer() == ark.subject()` and verifies the RSA-4096 PSS SHA-384 signature of the ASK against the ARK's modulus/exponent.
3. **VCEK ← ASK Signature**: Asserts `vcek.issuer() == ask.subject()`, rejects CA VCEKs (`vcek.is_ca()`), and verifies the signature on `vcek.tbs_certificate` against the ASK's RSA-4096 PSS key.
4. **Leaf P-384 Public Key Extraction**: Requires algorithm OID `1.2.840.10045.2.1` (`id-ecPublicKey`) with curve parameter OID `1.3.132.0.34` (`secp384r1`).
5. **AMD VCEK X.509 Extensions ([`extract_vcek_extensions`](file:///Users/ember/dev/breadstuffs/tee-verify/src/snp_chain.rs#L365-L406))**: Parses AMD Private Enterprise Number `3704` (`1.3.6.1.4.1.3704.1.*`) DER INTEGER / OCTET STRING extensions:
   - `1.3.6.1.4.1.3704.1.3.1` (`blSPL` — Bootloader SVN)
   - `1.3.6.1.4.1.3704.1.3.2` (`teeSPL` — PSP OS / TEE SVN)
   - `1.3.6.1.4.1.3704.1.3.3` (`snpSPL` — SNP firmware SVN)
   - `1.3.6.1.4.1.3704.1.3.8` (`ucodeSPL` — Microcode patch level)
   - `1.3.6.1.4.1.3704.1.3.9` (`fmcSPL` — Turin FMC SVN; required on Turin)
   - `1.3.6.1.4.1.3704.1.4` (`hwID` — 64-byte chip hardware ID)

#### Report↔VCEK Corroboration & Guest Policy Enforcement (`SnpPolicy`)
In [`SnpVerifier::verify_snp_at`](file:///Users/ember/dev/breadstuffs/tee-verify/src/snp.rs#L510-L639):
- **Report↔VCEK Cross-Check (Audit F2)**: Requires `report.reported_tcb == vcek.tcb` (`snp.rs:554-560`), `report.chip_id != [0u8; 64]` (rejecting `MaskChipId=1`), and `report.chip_id == vcek.hw_id` (`snp.rs:564-574`), preventing an attacker from pairing a report from a downgraded chip with a VCEK from a patched chip.
- **Guest Policy & VMPL Gates (Audit F1)**: [`SnpPolicy::default()`](file:///Users/ember/dev/breadstuffs/tee-verify/src/snp.rs#L397-L409) enforces:
  - `POLICY` bit 17 (`POLICY_RESERVED_MBO = 1 << 17`) must be `1` and bits `63:26` must be `0` (`snp.rs:581-594`).
  - `POLICY` bit 19 (`POLICY_DEBUG = 1 << 19`) must be `0` (`!policy.allow_debug`, `snp.rs:595-600`) — any debug-enabled guest (where hypervisor `SNP_DBG_DECRYPT`/`SNP_DBG_ENCRYPT` can read/write private memory) is unconditionally refused.
  - `POLICY` bit 18 (`POLICY_MIGRATE_MA = 1 << 18`) must be `0` (`!policy.allow_migrate_ma`, `snp.rs:601-606`).
  - `report.vmpl < 4` and `(policy.allowed_vmpls & (1 << report.vmpl)) != 0` where `allowed_vmpls = 0b0001` (`VMPL == 0` only, rejecting less-privileged VMPL 1..3 paravisor rings, `snp.rs:608-620`).
  - `report.guest_svn >= policy.min_guest_svn` (`snp.rs:621-627`).
  - `vcek.tcb.meets(&policy.min_tcb)` (evaluated against the VCEK's X.509 extension TCB, not the report body's `reported_tcb`).

---

### 1.4 Intel TDX / SGX DCAP (`TdxVerifier`)

Implemented in [`tee-verify/src/tdx.rs`](file:///Users/ember/dev/breadstuffs/tee-verify/src/tdx.rs#L1-L348), [`TdxVerifier`](file:///Users/ember/dev/breadstuffs/tee-verify/src/tdx.rs#L139-L298) verifies Intel TDX v4 and v5 quotes over Intel SGX DCAP (`dcap-qvl` v0.5.2):

- **Pinned Root Certificate**: [`INTEL_SGX_ROOT_CA_SHA256`](file:///Users/ember/dev/breadstuffs/tee-verify/src/tdx.rs#L52-L57) pins the SHA-256 digest of the DER-encoded Intel SGX Root CA (`CN=Intel SGX Root CA, O=Intel Corporation, C=US`):
  ```
  44A0196B2B99F889B8E149E95B807A350E7424964399E885A7CBB8CCFAB674D3
  ```
- **Quote Header & DCAP Verification ([`verify_tdx_core`](file:///Users/ember/dev/breadstuffs/tee-verify/src/tdx.rs#L194-L254))**:
  1. Parses the quote via `dcap_qvl::quote::Quote::parse(report_bytes)` and checks `quote.header.tee_type == TEE_TYPE_TDX` (`0x0000_0081`), rejecting SGX quotes (`0x0000_0000`) on the TDX lane.
  2. Parses the PEM chain in `collateral.root_ca_pem_chain`, locates the self-signed root (`cert.Subject == cert.Issuer`), and checks `SHA256(root.raw_der) == INTEL_SGX_ROOT_CA_SHA256`.
  3. Invokes `dcap_qvl::verify::verify(report_bytes, &self.collateral, self.now_secs)` to verify the QE Report ECDSA signature, PCK Certificate Chain, QE Identity, and TCB Info JSON collateral.
  4. Extracts the TD10 / TD15 report (`quote.report.as_td10()`), packing `mr_td` (48B), `rt_mr0` (48B), `rt_mr1` (48B), `rt_mr2` (48B), `rt_mr3` (48B), and `report_data` (64B) into [`TdxVerifiedReport`](file:///Users/ember/dev/breadstuffs/tee-verify/src/tdx.rs#L105-L120).
- **Measurement Folding & TCB Status**:
  - [`TdxVerifiedReport::folded_measurement()`](file:///Users/ember/dev/breadstuffs/tee-verify/src/tdx.rs#L127-L135) hashes the 4 static boot registers (excluding runtime `RTMR3`):
    $$\text{measurement} = \text{SHA-256}(\text{MRTD} \mathbin{\Vert} \text{RTMR}_0 \mathbin{\Vert} \text{RTMR}_1 \mathbin{\Vert} \text{RTMR}_2)$$
  - Default `accepted_statuses` contains only `{"UpToDate"}`; any other FMSPC TCB status (`OutOfDate`, `SWHardeningNeeded`, `ConfigurationNeeded`, `Revoked`) yields `TcbStatus::BelowPolicy`, which causes `TeeWitnessedPredicateVerifier` to refuse the turn.

---

### 1.5 Security Audit Findings (`docs/TEE-VERIFY-AUDIT-2026-07-25.md`)

On 2026-07-25, an internal adversarial security audit ([`docs/TEE-VERIFY-AUDIT-2026-07-25.md`](file:///Users/ember/dev/breadstuffs/docs/TEE-VERIFY-AUDIT-2026-07-25.md#L1-L407)) catalogued 14 findings (`F1`–`F14`) across `tee-verify`, `tee-produce`, and `dregg-discharge-gateway`:
- **F1 (CRITICAL — SEV-SNP `POLICY` / `VMPL` / `GUEST_SVN` unvalidated)**: `SnpAttestationReport` originally discarded bytes `0x008..0x034`, permitting `DEBUG=1` or `VMPL=3` reports. **Remediated** in commit `4d98292c2` (2026-09-30) via `SnpPolicy`.
- **F2 (CRITICAL — SEV-SNP `reported_tcb` and `chip_id` not cross-checked against VCEK OIDs)**: Originally allowed mixing a VCEK from a patched machine with a report from an unpatched machine if signed by the same key, or accepting `MaskChipId=1` zeroed `chip_id`. **Remediated** in commit `4d98292c2` (`snp.rs:554-574`).
- **F3 (HIGH — SEV-SNP CRL checking)**: Added `ark_crl_der` / `ask_crl_der` checking on `SnpVerifier` in commit `4d98292c2` (`snp.rs:463-474`, `543-552`).
- **F10 (MEDIUM — Nitro freshness bypass when `now_secs == 0`)**: **Remediated** in commit `a9d5df4db` (2026-09-30) so `NitroVerifier::new()` seeds wall-clock time (`SystemTime::now()`) and `check_nitro_freshness` fails closed on `now_secs == 0` or future-dated documents.
- **F11 / F12 / F14 (CRITICAL/HIGH — Discharge gateway condition validation)**: **Remediated** in commit `551fc897f` (2026-09-30).

---

### 1.6 Enclave Quote Producer (`tee-produce` & `NitroNsmBackend`)

In [`tee-produce/src/lib.rs`](file:///Users/ember/dev/breadstuffs/tee-produce/src/lib.rs#L1-L263) and [`tee-produce/src/nsm.rs`](file:///Users/ember/dev/breadstuffs/tee-produce/src/nsm.rs#L1-L95) (introduced in commit `ad33c9247`, 2026-07-12):
- [`NitroNsmBackend`](file:///Users/ember/dev/breadstuffs/tee-produce/src/nsm.rs#L28-L61) (gated behind `--features nitro-nsm` on Linux) opens `/dev/nsm` via `aws_nitro_enclaves_nsm_api::driver::nsm_init()` (failing closed if `fd < 0`), issues `nsm_process_request(fd, Request::Attestation { user_data: Some(ByteBuf::from(report_data.to_vec())), nonce: None, public_key: None })`, closes the descriptor with `nsm_exit(fd)`, and returns the raw `COSE_Sign1` bytes from `Response::Attestation { document }`.
- [`QuoteProducer::produce_predicate_proof`](file:///Users/ember/dev/breadstuffs/tee-produce/src/lib.rs#L118-L125) binds a 32-byte `report_data` commitment (matching `grain_turn::ATTESTATION_SLOT`) into the hardware quote and wraps it via `encode_tee_proof(self.kind(), &raw)`.
- [`serve_single_request`](file:///Users/ember/dev/breadstuffs/tee-produce/src/lib.rs#L207-L250) serves the enclave quote over newline-delimited JSON (`ProduceRequest { report_data_hex }` → `ProduceResponse { ok, quote_kind, proof_hex, error }`, capped at `MAX_FRAME_BYTES = 1 << 20` bytes) across an `AF_VSOCK` or TCP stream.

---

## 2. Confidential GPU Inference & Post-Quantum E2EE (`dregg-chutes-e2ee` & `attest-check`)

### 2.1 Confidential GPU TDX Attestation (`dregg-chutes-e2ee/src/attest.rs`)

[`dregg-chutes-e2ee`](file:///Users/ember/dev/breadstuffs/dregg-chutes-e2ee/src/lib.rs#L1-L87) (commits `9d5d06853` 2026-07-23, `6f38efbe3` 2026-07-26, `4bcb934a3` 2026-07-27) implements end-to-end encrypted confidential LLM inference against GPU instances running inside Intel TDX Confidential VMs with NVIDIA H200/B200 TEE GPUs.

Before any prompt is encrypted, [`attest_chute`](file:///Users/ember/dev/breadstuffs/dregg-chutes-e2ee/src/attest.rs#L140-L249) executes the hardware attestation handshake:
1. Generates a fresh 32-byte random nonce (`nonce_bytes: [u8; 32]`) and encodes it as a 64-character lowercase hex string (`nonce_hex`).
2. Fetches `GET /e2e/instances/{chute_id}` (returning instance list with `instance_id` and `e2e_pubkey` Base64 ML-KEM-768 public key) and `GET /chutes/{chute_id}/evidence?nonce={nonce_hex}` (returning per-instance `quote` Base64 Intel TDX v4 quote, `gpu_evidence`, and `collateral`).
3. Calls [`verify_instance_evidence`](file:///Users/ember/dev/breadstuffs/dregg-chutes-e2ee/src/attest.rs#L261-L320), which invokes `TdxVerifier::verify_tdx_core(&quote_bytes)` followed by [`TdxVerifier::apply_chutes_bindings`](file:///Users/ember/dev/breadstuffs/tee-verify/src/tdx.rs#L262-L298).
4. **Anti-MITM Session Binding ([`chutes_report_data_binding`](file:///Users/ember/dev/breadstuffs/tee-verify/src/tdx.rs#L332-L337))**:
   - Validates that `nonce_hex` is 64 hex characters and `e2e_pubkey_b64` Base64-decodes to exactly `CHUTES_MLKEM768_PK_LEN = 1184` bytes (`tdx.rs:268-277`).
   - Computes the 32-byte binding hash over the ASCII bytes of the nonce and the Base64 public key:
     $$\text{expected} = \text{SHA-256}(\text{ascii}(\text{nonce\_hex}) \mathbin{\Vert} \text{ascii}(\text{e2e\_pubkey\_b64}))$$
   - Verifies in constant time (`subtle::ConstantTimeEq`) that the hardware-signed TDX quote's `report_data[0..32]` (at byte offset `568` of the TDX v4 quote) equals `expected`:
     ```rust
     if report.report_data[..32].ct_eq(&expected).unwrap_u8() != 1 {
         return Err("tdx-verify: Chutes report_data[..32] != SHA256(nonce || e2e_pubkey) — MITM or stale quote".into());
     }
     ```
   - This prevents the untrusted API gateway from substituting its own ML-KEM-768 keypair or replaying a stale quote from another session.
5. **Measurement Registry & TCB Floor**: Checks `(mr_td, rt_mr0, rt_mr1, rt_mr2)` against [`ChutesMeasurements`](file:///Users/ember/dev/breadstuffs/tee-verify/src/tdx.rs#L79-L102) and requires `report.tcb_ok` (unless `allow_tcb_ProceedAnyway` is explicitly set for dev collateral).
6. Caches the resulting [`AttestedSession`](file:///Users/ember/dev/breadstuffs/dregg-chutes-e2ee/src/session.rs#L17-L29) in [`SessionCache`](file:///Users/ember/dev/breadstuffs/dregg-chutes-e2ee/src/session.rs#L53-L108) with a 30-minute TTL (`DEFAULT_TTL_SECS = 1800`) and automatic single-retry eviction on HTTP `466` (instance key rotation).

---

### 2.2 Post-Quantum ML-KEM-768 + HKDF-SHA256 + ChaCha20-Poly1305 Envelope (`dregg-chutes-e2ee/src/crypto.rs`)

Implemented in [`dregg-chutes-e2ee/src/crypto.rs`](file:///Users/ember/dev/breadstuffs/dregg-chutes-e2ee/src/crypto.rs#L1-L265), prompt encryption and streaming response decryption use NIST FIPS 203 **ML-KEM-768** (`pqcrypto_mlkem::mlkem768`):

- **Key & Wire Sizes ([`crypto.rs:23-32`](file:///Users/ember/dev/breadstuffs/dregg-chutes-e2ee/src/crypto.rs#L23-L32))**:
  - `MLKEM_PK_SIZE = 1184` bytes
  - `MLKEM_SK_SIZE = 2400` bytes
  - `MLKEM_CT_SIZE = 1088` bytes
  - `NONCE_SIZE = 12` bytes
  - `TAG_SIZE = 16` bytes
  - `BLOB_HEADER_SIZE = 1100` bytes (`1088 + 12`)
- **Request Encryption ([` build_encrypted_request`](file:///Users/ember/dev/breadstuffs/dregg-chutes-e2ee/src/crypto.rs#L65-L120))**:
  1. Generates a single-use ephemeral ML-KEM-768 keypair `(response_pk, response_sk) = mlkem768::keypair()` so the enclave can encapsulate its response back to the client.
  2. Injects `"e2e_response_pk": base64(response_pk)` into the JSON request object and compresses the UTF-8 JSON bytes with `flate2::write::GzEncoder` (`Compression::default()`).
  3. Encapsulates to the attested enclave's `instance_pk`: `(shared_secret, mlkem_ct) = mlkem768::encapsulate(&pk)` (`shared_secret` = 32 bytes, `mlkem_ct` = 1088 bytes).
  4. Derives the 32-byte symmetric key via [`hkdf_derive_key`](file:///Users/ember/dev/breadstuffs/dregg-chutes-e2ee/src/crypto.rs#L52-L58):
     $$\text{key}_{\text{req}} = \text{HKDF-SHA256}\bigl(\text{salt} = \text{mlkem\_ct}[0..16],\;\text{ikm} = \text{shared\_secret},\;\text{info} = \texttt{"e2e-req-v1"}\bigr)$$
  5. Generates a 12-byte random nonce and encrypts the gzipped payload with `ChaCha20Poly1305`, serializing the wire envelope as:
     $$\text{blob} = \text{mlkem\_ct (1088B)} \mathbin{\Vert} \text{nonce (12B)} \mathbin{\Vert} \text{ciphertext} \mathbin{\Vert} \text{poly1305\_tag (16B)}$$
  6. Transmits `blob` to `POST https://api.chutes.ai/e2e/invoke` with headers `X-Chute-Id`, `X-Instance-Id`, and `Content-Type: application/octet-stream` ([`client.rs:148-159`](file:///Users/ember/dev/breadstuffs/dregg-chutes-e2ee/src/client.rs#L148-L159)).
- **Non-Streaming & SSE Streaming Response Decryption ([`decrypt_response`](file:///Users/ember/dev/breadstuffs/dregg-chutes-e2ee/src/crypto.rs#L126-L156), [`StreamDecryptor`](file:///Users/ember/dev/breadstuffs/dregg-chutes-e2ee/src/crypto.rs#L168-L250))**:
  - For non-streaming replies, decapsulates `mlkem_ct = blob[..1088]` using `response_sk`, derives `key_resp` via HKDF-SHA256 with `info = b"e2e-resp-v1"`, decrypts with `ChaCha20Poly1305`, and gunzips (capped at `MAX_DECOMPRESSED_BYTES = 64 * 1024 * 1024` = 64 MiB to prevent gzip-bomb OOM).
  - For SSE streaming replies, the first event `data: {"e2e_init": "<b64 mlkem_ct>"}` is decapsulated via [`StreamDecryptor::from_init_b64`](file:///Users/ember/dev/breadstuffs/dregg-chutes-e2ee/src/crypto.rs#L174-L202) using `info = b"e2e-stream-v1"` (retaining only the 32-byte `stream_key`), and each subsequent `data: {"e2e": "<b64 nonce(12) || ct || tag(16)>"}` chunk is authenticated and decrypted via [`StreamDecryptor::decrypt_chunk_b64`](file:///Users/ember/dev/breadstuffs/dregg-chutes-e2ee/src/crypto.rs#L206-L224).

---

### 2.3 Standalone 6-Link Provenance Verifier (`attest-check` / `dungeon-attest-check`)

In commit `6f38efbe3` (2026-07-26, *"the attested narration was visible and UNCHECKABLE — now the quote outlives the process, and the rate is the provider's own"*), [`dregg-chutes-e2ee/src/narrator_backend.rs`](file:///Users/ember/dev/breadstuffs/dregg-chutes-e2ee/src/narrator_backend.rs#L36-L148) was wired to persist a self-contained [`TeeProvenanceRecord`](file:///Users/ember/dev/breadstuffs/dregg-chutes-e2ee/src/narrator_backend.rs#L36-L83) (`raw_quote_b64`, `collateral`, `nonce_hex`, `e2e_pubkey_b64`, `expected_measurements`, `tee_provenance_commit_hex`) alongside every attested narrator receipt.

The standalone verifier [`attest-check/src/lib.rs`](file:///Users/ember/dev/breadstuffs/attest-check/src/lib.rs#L1-L512) and CLI binary [`attest-check/src/bin/dungeon-attest-check.rs`](file:///Users/ember/dev/breadstuffs/attest-check/src/bin/dungeon-attest-check.rs#L1-L263) verify **six independent cryptographic provenance links** ([`verify_record`](file:///Users/ember/dev/breadstuffs/attest-check/src/lib.rs#L435-L458)):

1. **Link 1 — `quote digest` ([`check_quote_digest`](file:///Users/ember/dev/breadstuffs/attest-check/src/lib.rs#L186-L223))**: Base64-decodes `raw_quote_b64`, verifies `quote_bytes.len() == record.quote_len` and `quote_bytes.len() >= MIN_TDX_V4_QUOTE_LEN (584)`, and checks `hex(SHA-256(quote_bytes)) == record.quote_sha256_hex`.
2. **Link 2 — `session binding` ([`check_session_binding`](file:///Users/ember/dev/breadstuffs/attest-check/src/lib.rs#L228-L273))**: Checks `nonce_hex.len() == 64` (valid hex), Base64-decodes `e2e_pubkey_b64` and checks `pk_bytes.len() == 1184` (ML-KEM-768 public key size), reads `report_data[0..32]` directly from the TDX v4 quote at byte offset `TD10_REPORT_DATA_OFFSET = 568` (`48 + 520`), and verifies `report_data[0..32] == SHA-256(nonce_hex || e2e_pubkey_b64)` == `record.report_data_32_hex`.
3. **Link 3 — `measurement registry` ([`check_measurement_registry`](file:///Users/ember/dev/breadstuffs/attest-check/src/lib.rs#L278-L353))**: Parses the TD10 report body, checks `mr_td`, `rt_mr0`, `rt_mr1`, `rt_mr2` against the record's hex fields, checks `SHA-256(MRTD || RTMR0 || RTMR1 || RTMR2) == record.folded_measurement_hex`, and verifies membership in `expected_measurements` (`ChutesMeasurements`).
4. **Link 4 — `receipt commitment` ([`check_receipt_commitment`](file:///Users/ember/dev/breadstuffs/attest-check/src/lib.rs#L357-L374))**: Recomputes the domain-separated BLAKE3 receipt commitment (`TeeProvenanceRecord::recompute_commit_hex`, domain `"dungeon-on-dregg/tee-provenance-v1:"`) over `(chute_id, instance_id, quote_sha256_hex, folded_measurement_hex, report_data_32_hex, tcb_status, verified_at_unix_ms)` and checks equality with `tee_provenance_commit_hex`.
5. **Link 5 — `Intel root pin` ([`check_intel_root_pin`](file:///Users/ember/dev/breadstuffs/attest-check/src/lib.rs#L379-L406))**: Parses `collateral.root_ca_pem_chain`, locates the self-signed root (`cert.Subject == cert.Issuer`), and verifies `SHA-256(root.raw_der) == INTEL_SGX_ROOT_CA_SHA256` (`44a0196b...674d3`).
6. **Link 6 — `DCAP signature chain` ([`check_dcap_chain`](file:///Users/ember/dev/breadstuffs/attest-check/src/lib.rs#L411-L430))**: Reconstructs `TdxVerifier` with the embedded collateral at `verified_at_unix_ms / 1000` (with a 60s skew fallback for leaf quote issuance skew) and runs `verifier.verify_tdx_core(&quote_bytes)`.

The CLI (`dungeon-attest-check`) maps [`OverallStatus`](file:///Users/ember/dev/breadstuffs/attest-check/src/lib.rs#L84-L108) to deterministic exit codes: `0` (`Verified` — all 6 links `PASS`), `1` (`Broken` — any link `FAIL`), `2` (CLI usage / I/O error), and `3` (`Unauthenticated` — Link 6 `SKIP` when no offline collateral bundle was captured).

---

## 3. Why TEE Alone Is Not Enough (`degg-research` Residual Trust Proof)

In [`/Users/ember/dev/degg-research`](file:///Users/ember/dev/degg-research), Ember proved mathematically and empirically why a hardware TEE / shielded dark pool without a zero-knowledge conservation and uniform-clearing proof leaves a massive **residual trust** surface.

### 3.1 The `dark-fba/n4-k4-q15/v0` Model & `price_tie_low` Witness

Tracked in [`docs/VERDICTS.md`](file:///Users/ember/dev/degg-research/docs/VERDICTS.md#L15-L34) (**Verdicts V3 and V4**, commit `ac77a4d`, 2026-08-18) and [`experiments/shielded-baseline/tests/residual_trust.rs`](file:///Users/ember/dev/degg-research/experiments/shielded-baseline/tests/residual_trust.rs#L1-L246):
- **Market Shape (`dark-fba/n4-k4-q15/v0`)**:
  - `SLOT_COUNT = 4` order slots (`i ∈ {0, 1, 2, 3}`), 4 owners (`owner_id = i`).
  - `TICK_COUNT = 4` discrete price ticks (`0, 1, 2, 3`), plus `ClearedTick::NoCross` (5 total tick states).
  - `QUANTITY_MAX = 15` (`q_i ∈ 0..=15`), so maximum single-side aggregate quantity is `MAX_SIDE_TOTAL = 4 * 15 = 60` ([`owner.rs:9`](file:///Users/ember/dev/degg-research/experiments/shielded-baseline/src/owner.rs#L9)).
- **The `price_tie_low()` Batch ([`tests/common/mod.rs:28-36`](file:///Users/ember/dev/degg-research/experiments/shielded-baseline/tests/common/mod.rs#L28-L36))**:
  - Slot 0: `BookOrder::exact(0, Side::Buy, limit_tick = 2, quantity = 4)`
  - Slot 1: `BookOrder::exact(1, Side::Sell, limit_tick = 1, quantity = 4)`
  - Slot 2: padding `Side::Buy`, `limit_tick = 0`, `quantity = 0`
  - Slot 3: padding `Side::Sell`, `limit_tick = 3`, `quantity = 0`
  - Honest uniform batch clearing result: `ClearedTick::Tick(1)`, `volume = 4`, `fills = [4, 4, 0, 0]`.

### 3.2 What Each Participant Can Check Locally (`owner::audit`)

In a shielded / TEE-only dark pool without a validity proof, each participant $i$ sees only the public batch header `(cleared_tick, volume, delivery_root, batch_digest)` and their own private fill opening `fill_i` (with Merkle path to `delivery_root`). In [`experiments/shielded-baseline/src/owner.rs`](file:///Users/ember/dev/degg-research/experiments/shielded-baseline/src/owner.rs#L53-L162), each owner runs the strongest possible 8-point local audit (`owner::audit`):
1. `BatchDigestMismatch`: header digest matches the committed order slots.
2. `PublicationInvalid`: `volume <= SLOT_COUNT * QUANTITY_MAX` (`60`) and `NoCross ==> volume == 0`.
3. `InclusionFailed`: Merkle inclusion proof of `(slot, owner_id, fill_i, salt_i)` against `delivery_root`.
4. `Overfill`: `fill_i <= order.quantity`.
5. `BelowMinimum`: `fill_i == 0 || fill_i >= order.min_fill`.
6. `VolumeBelowFill`: `fill_i <= header.volume` (since a single participant's fill cannot exceed total cleared volume).
7. `CrossedWithoutFill`: if `header.cleared_tick == NoCross`, `fill_i == 0`; if `Tick(p)` is worse than `order.limit_tick`, `fill_i == 0`.
8. `ProRataImplausible` ([`pro_rata_feasible`](file:///Users/ember/dev/degg-research/experiments/shielded-baseline/src/owner.rs#L172-L202)): if the order is eligible at `Tick(p)`, checks whether there exists *any* hypothetical aggregate side total $T \in [\max(q_i, V), 60]$ and hypothetical pre-OrderId-tiebreak prefix $B \in [0, \min(\text{slot}, (V \cdot T) \bmod T)]$ such that integer pro-rata rationing $\lfloor \frac{V \cdot q_i}{T} \rfloor + \mathbb{I}[\text{tiebreak}]$ produces `fill_i`.

### 3.3 The Exhaustive Forgery Theorem: **377 out of 1,125** Outcomes Survive

In [`exhaust_price_tie_low_forgeries`](file:///Users/ember/dev/degg-research/experiments/shielded-baseline/tests/residual_trust.rs#L118-L216), the test enumerates the entire candidate outcome space for `price_tie_low()`:
- $5$ cleared-tick values (`NoCross`, `Tick(0)`, `Tick(1)`, `Tick(2)`, `Tick(3)`)
- $9$ volume values ($V \in 0..=8$, where $8 = \sum q_i$)
- $5$ fill values for Buyer 0 ($f_0 \in 0..=4$)
- $5$ fill values for Seller 1 ($f_1 \in 0..=4$)
- $1$ fill value for Padding 2 ($f_2 = 0$) and $1$ fill value for Padding 3 ($f_3 = 0$)
- Total candidate space: $5 \times 9 \times 5 \times 5 \times 1 \times 1 = \mathbf{1,125}$ candidate outcomes.

For each candidate `(cleared_tick, volume, fills)`, [`forge_outcome`](file:///Users/ember/dev/degg-research/experiments/shielded-baseline/tests/residual_trust.rs#L35-L78) builds a valid Merkle `DeliveryCommitment` and `ShieldedReceipt` and runs `receipt.public_check(&batch)` plus `owner::audit` for all 4 owners. The exact asserted result (`residual_trust.rs:159-215`):

```rust
assert_eq!(total_candidates, 1_125);
assert_eq!(accepted.len(), 377);
assert_eq!(distinct_headers.len(), 33);
```

- **377 out of 1,125** outcomes (`33.5%`, or **376 false accepts** besides the 1 honest clearing `(Tick(1), 4, [4, 4, 0, 0])`) pass the public check and **all four owners' local audits simultaneously**.
- **All 33 well-formed `(cleared_tick, volume)` pairs** (`1` for `NoCross` at $V=0$, plus $4 \times 8 = 32$ for `Tick(0..=3)` at $V \in 1..=8$) admit at least one fill vector that passes every owner's local check!
- Five concrete pathology classes are exhibited in [`residual_trust.rs`](file:///Users/ember/dev/degg-research/experiments/shielded-baseline/tests/residual_trust.rs#L81-L115):
  1. **Silent Suppression (`NoCross`, $V=0$, `fills = [0, 0, 0, 0]`)**: The operator claims no cross occurred even though Buyer 0 (limit 2) and Seller 1 (limit 1) crossed by 1 tick.
  2. **Volume Inflation (`Tick(1)`, $V=8$, `fills = [4, 4, 0, 0]`)**: The operator reports double the actual cleared volume ($V=8$ when each side only has 4 units).
  3. **Conservation Violation / Unbalanced Fill (`Tick(1)`, $V=4$, `fills = [4, 2, 0, 0]`)**: Buyer 0 receives 4 units while Seller 1 only delivers 2 units ($\sum f_{\text{buy}} = 4 \neq 2 = \sum f_{\text{sell}}$). Seller 1 accepts `fill = 2` because $T_{\text{sell}} = 8$ is plausible to Seller 1 in isolation!
  4. **Limit Violation Hidden in Aggregate (`Tick(0)`, $V=4$, `fills = [4, 0, 0, 0]`)**: Cleared below Seller 1's limit of 1; Seller 1 receives 0 (valid for an out-of-the-money seller) and cannot see that Buyer 0 was filled against nobody.
  5. **Worse-Price Clearing (`Tick(2)`, $V=4$, `fills = [4, 4, 0, 0]`)**: Cleared at `Tick(2)` instead of the canonical tie-broken `Tick(1)`.

As [`docs/VERDICTS.md`](file:///Users/ember/dev/degg-research/docs/VERDICTS.md#L19-L26) concludes:
> **V3 (`shielded-alone-insufficient`, REFUTED):** *"An unproved shielded matcher can forge **377 of 1,125** outcomes (`376` false accepts) and all **33 of 33** well-formed `(cleared_tick, volume)` pairs on `price_tie_low` while passing every owner's local fill check."*  
> **V4 (`shielded-plus-proof-Adopted`, ADOPTED):** Pairing the shielded channel with a zero-knowledge proof of the canonical clearing circuit (`verify_ canonical_batch`) collapses the 376 forgeries to **0**.

---

## 4. Bare-Metal `seL4` Microkit Protection Domains & OS Sandboxing (`sel4/`, `grain-jail`, `nanodregg/sandbox`)

### 4.1 Bare-Metal `seL4` Microkit 2.2.0 Architecture (`breadstuffs/sel4/`)

Introduced on 2026-06-13 (commits `8ef312b5e`, `a744edfc0`, `2490e7f33`, `f49b87b35`, `9dfdfea27`), [`/Users/ember/dev/breadstuffs/sel4/`](file:///Users/ember/dev/breadstuffs/sel4/README.md#L1-L276) boots a multi-Protection-Domain Dregg system directly on top of the formally verified **seL4 microkernel** (via seL4 Microkit SDK 2.2.0) on both **ARM64 (`aarch64-sel4-microkit`, QEMU `virt,virtualization=on`, Cortex-A53)** and **RISC-V 64 (`riscv64-sel4-microkit`, QEMU `virt`, `rv64imac_zicsr_zifencei`)**.

#### Protection Domain Topology (`dregg.system` & `riscv-stark.system`)
In [`sel4/dregg.system`](file:///Users/ember/dev/breadstuffs/sel4/dregg.system#L1-L163), the static capability topology is partitioned into 6 isolated Protection Domains (PDs) communicating strictly via seL4 notification channels and page-bounded shared memory regions (`0x4_000_000`–`0x4_020_000`):

| PD Name | Priority | Budget / Period | Program Image | Role & Shared Memory |
|---|---|---|---|---|
| `verifier` | `100` | `1000 / 1000` | `verifier-pd.elf` | Lean-free `no_std` verifier checking turn format, conservation, capabilities, and STARK proofs (`turn_inbox` `r` at `0x4_000_000`, `verdict_outbox` `rw` at `0x4_001_000`) |
| `executor` | `120` | `5000 / 10000` | `executor-pd.elf` | Links `libdregg_lean_v2.a` (2,703-symbol `leanc` archive) + bare-metal C runtime shim (`setjmp`/`longjmp` bump-heap rollback) to run `dregg_exec_full_forest` |
| `persist` | `80` | — | `persist-pd.elf` | Append-only hash-chained journal over shared memory (`persist_inbox`, `persist_outbox`) |
| `net` | `60` | — | `net-pd.elf` | MMIO driver (`0x0a003000`, IRQ `79`) for `virtio-net-device` with DMA ring at `0x4_010_000` |
| `net_client`| `59` | — | `net-client-pd.elf` | Bridges `net` rx/tx rings into the executor turn inbox |
| `app` | `50` | — | `app-pd.elf` | Untrusted application PD holding only a capability to submit turns (`ch 1`) |

#### Proving & Verifying a Real BabyBear + BLAKE3 + FRI STARK Inside PD 3 (`verifier-stark`)
In [`sel4/dregg-pd/verifier-stark/src/main.rs`](file:///Users/ember/dev/breadstuffs/sel4/dregg-pd/verifier-stark/src/main.rs#L1-L143) (and its original self-test in commit `7cb8626a41` on 2026-06-15, plus [`sel4/riscv-stark.system`](file:///Users/ember/dev/breadstuffs/sel4/riscv-stark.system#L1-L14)), PD 3 runs a 64 MiB static bump-allocated heap (`#[global_allocator] static HEAP: LockedHeap`, `HEAP_BYTES = 64 * 1024 * 1024`) in `.bss`:
- **Kernel Patch (`0001-2mib-elf-image-pages.patch`)**: Because the 64 MiB `.bss` heap exceeds Microkit's default 4 KiB page mapping loop limit, Ember patched the Microkit loader to map 2 MiB large pages for the PD ELF image.
- **Original Self-Test (`7cb8626a41`)**: Defined a 2-column Plonky3 `CounterSquareAir` (`col 0`: counter $0, 1, \dots, N-1$ with constraint $(c' - c - 1)$ on transitions; `col 1`: $c^2$ with constraint $s - c \cdot c = 0$ on every row) over `BabyBear` (`p3_baby_bear`), committed the trace with `SerializingHasher64<Blake3>` (`p3_blake3`) + `CompressionFunctionFromHasher` (`2 -> 32 bytes`), opened via `TwoAdicFriPcs` (`log_blowup = 2`, `num_queries = 28`, `proof_of_work_bits = 8`), and generated & verified a **78,135-byte STARK proof** on bare-metal ARM64 and RISC-V64 inside the seL4 protection domain.
- **Cutover to Lean-Emitted Descriptor Prover (`dd038c08e0`, 2026-07-09)**: Replaced the hand-written `CounterSquareAir` with `dregg_p3_pcs::prove_descriptor` and `dregg_p3_pcs::verify_descriptor` over `LEAN_FACT_HASH_IR_V2_JSON` (`Dregg2.Circuit.FactHashAir.factHashIrV2Json`, 6 columns, `pub_inputs = [10, 20, 30, 40, 240]`), proving and verifying the Lean-emitted AIR descriptor inside the seL4 PD (`main.rs:88-127`).

---

### 4.2 Unifying seL4 CNode Caps and Distributed Dregg Caps (`dregg-firmament` & `Dregg2.Firmament`)

In [`sel4/dregg-firmament/src/lib.rs`](file:///Users/ember/dev/breadstuffs/sel4/dregg-firmament/src/lib.rs#L1-L343), [`Capability`](file:///Users/ember/dev/breadstuffs/sel4/dregg-firmament/src/lib.rs#L172-L246) unifies hardware-enforced seL4 capabilities and cryptographically-enforced distributed Dregg capabilities behind one handle:

```rust
#[derive(Clone, Debug, PartialEq, Eq)]
pub enum Target {
    /// Target is a Protection Domain on THIS machine (`ch: u8` = Microkit channel 0..63).
    Local { ch: u8 },
    /// Target is a cell across a `quorum_size`-of-N federation (`cell_id`, `token_hash`, `quorum_size`).
    Distributed {
        cell_id: [u8; 32],
        token_hash: [u8; 32],
        quorum_size: u16,
    },
    /// Target is a GPU surface at `surface_idx` in the compositor's table.
    Surface { surface_idx: u16, quorum_size: u16 },
    /// Target is a host-OS child process confined by Seatbelt/seccomp (`pd_id`, `door_fd`).
    HostPd { pd_id: u8, door_fd: i32 },
}

#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub struct Bounds {
    pub revocation_immediate: bool,
    pub commit_synchronous: bool,
    pub n: u16,
}
```

- [`Capability::attenuate(&self, mask: Rights) -> Option<Self>`](file:///Users/ember/dev/breadstuffs/sel4/dregg-firmament/src/lib.rs#L186-L194) checks `is_attenuation(self.rights, mask)` (`(granted.0 & !held.0) == 0`, i.e., `granted ⊆ held`) identically regardless of backing (`Target`), mirroring `seL4_CNode_Mint` rights masking locally and Macaroon/Biscuit caveat append remotely.
- [`Capability::bounds(&self)`](file:///Users/ember/dev/breadstuffs/sel4/dregg-firmament/src/lib.rs#L204-L245) returns the exact synchrony gradation: at `n == 1` (`Target::Local`, `Target::HostPd`, or `Target::Distributed { quorum_size: 1 }`), `revocation_immediate = true` and `commit_synchronous = true`.

#### Lean 4 Formalization (`Dregg2.Firmament.CapGradation` & `SeL4Abstract`)
1. **[`metatheory/Dregg2/Firmament/CapGradation.lean`](file:///Users/ember/dev/breadstuffs/metatheory/Dregg2/Firmament/CapGradation.lean#L1-L261)**:
   - `theorem attenuate_decision_backing_agnostic` (lines 112–115):
     ```lean
     theorem attenuate_decision_backing_agnostic (t₁ t₂ : Target) (r mask : Rights) :
         (attenuate ⟨t₁, r⟩ mask).isSome = (attenuate ⟨t₂, r⟩ mask).isSome := by
       simp [attenuate]
     ```
   - `theorem attenuate_iff_grantOk` (lines 125–129):
     ```lean
     theorem attenuate_iff_grantOk (c : Capability) (mask : Rights) :
         (attenuate c mask).isSome = true ↔ grantOk c.rights mask = true := by
       simp [attenuate, isAttenuation, grantOk]
     ```
   - `theorem no_amplification` (lines 134–141):
     ```lean
     theorem no_amplification (c c' : Capability) (mask : Rights)
         (h : attenuate c mask = some c') :
         ∀ a, a ∈ c'.rights → a ∈ c.rights := by ...
     ```
   - `theorem distributed_collapses_at_one` (lines 166–170):
     ```lean
     theorem distributed_collapses_at_one (cid : CellId) (th : Nat) (ch : ChannelId) (r : Rights) :
         bounds ⟨.distributed cid th 1, r⟩ = bounds ⟨.local ch, r⟩ := by
       simp [bounds]
     ```
2. **[`metatheory/Dregg2/Firmament/SeL4Abstract.lean`](file:///Users/ember/dev/breadstuffs/metatheory/Dregg2/Firmament/SeL4Abstract.lean#L1-L280)** (transcribing Data61 `l4v@e2f32e54` `spec/abstract/Structures_A.thy` and `CSpaceAcc_A.thy`):
   - `theorem seL4_derive_cap_non_amplifying` (lines 128–134):
     ```lean
     theorem seL4_derive_cap_non_amplifying (c : SeL4Cap) (mask : CapRights) :
         ∀ r, r ∈ (maskCapRights mask c).rights → r ∈ c.rights :=
       maskCapRights_subset c mask
     ```
   - `theorem alpha_total_iff_used` (lines 195–199):
     ```lean
     theorem alpha_total_iff_used (c : SeL4Cap) :
         (α c).isSome = true ↔ UsedSeL4Cap c := by
       cases c <;> simp [α, UsedSeL4Cap]
     ```
   - `theorem dregg_executor_cap_authority_grounded_in_seL4` (lines 253–269):
     ```lean
     theorem dregg_executor_cap_authority_grounded_in_seL4
         (c : SeL4Cap) (mask : CapRights) (fc fc' : CapGradation.Capability)
         (hα : α c = some fc)
         (h_mint : α (maskCapRights mask c) = some fc') :
         (∀ r, r ∈ fc'.rights → r ∈ fc.rights) ∧
         fc'.target = fc.target := by ...
     ```

---

### 4.3 Host-OS Sandboxing (`grain-jail` & `nanodregg/sandbox`)

#### `grain-jail` & `dregg-firmament/src/sandbox.rs`
In [`sel4/dregg-firmament/src/sandbox.rs`](file:///Users/ember/dev/breadstuffs/sel4/dregg-firmament/src/sandbox.rs#L1-L400) and [`grain-jail/src/jail.rs`](file:///Users/ember/dev/breadstuffs/grain-jail/src/jail.rs#L1-L220) (commits `5a707ec02`, `44e272708`, `ab659504d` on 2026-07-05..06; hardened in `292829518` and `3ecfd0bd1` on 2026-09-30):
- [`ProcessKernel::spawn_pd`](file:///Users/ember/dev/breadstuffs/sel4/dregg-firmament/src/sandbox.rs#L278-L355) creates an IPC `socketpair(AF_UNIX, SOCK_STREAM)` per channel, forks the child process, closes every inherited file descriptor except `{0, 1, 2}` and the PD's assigned channel descriptors (`close_all_fds_except`), and applies [`confine_current_process()`](file:///Users/ember/dev/breadstuffs/sel4/dregg-firmament/src/sandbox.rs#L105-L120) before executing the PD closure:
  - **macOS (`apply_seatbelt`)**: Calls `sandbox_init(profile, 0, &mut errbuf)` with the deny-by-default SBPL profile:
    ```scheme
    (version 1)
    (deny default)
    (allow process-info* (target self))
    (allow sysctl-read)
    (allow mach-lookup (global-name "com.apple.system.logger"))
    ```
    Any subsequent `File::open`, `TcpStream::connect`, or `Command::new` fails with `EPERM`.
  - **Linux (`apply_linux_sandbox`)**: Sets `prctl(PR_SET_NO_NEW_PRIVS, 1)`, unshares `CLONE_NEWUSER | CLONE_NEWNET | CLONE_NEWNS | CLONE_NEWIPC`, applies Landlock ABI v1 with empty ruleset (`LANDLOCK_ACCESS_FS_READ_FILE | WRITE_FILE | EXECUTE` handled and denied), and installs a classic BPF seccomp filter (`SECCOMP_SET_MODE_FILTER`) that permits only `read`, `write`, ` recvmsg`, `sendmsg`, `futex`, `mmap`, `munmap`, `mprotect`, `brk`, `rt_sigreturn`, `exit_group`, `clock_gettime`, `getrandom`, `sched_yield`, `close`, `poll`/`ppoll`, and `ioctl(fd, FIONBIO)` (`0x5421` matched on the full 64-bit request per commit `292829518`), or traps to a supervisor fd via `SECCOMP_RET_USER_NOTIF` (`provider_door`).
- [`grain-jail/src/lib.rs`](file:///Users/ember/dev/breadstuffs/grain-jail/src/lib.rs#L140-L246) wraps the confined child in [`ConfinedBrain<C: BodyChannel>`](file:///Users/ember/dev/breadstuffs/grain-jail/src/lib.rs#L142-L148): the jailed process holds **zero secret keys** and receives only opaque state commitments (`WorldView { tick, current_state_commitment, available_actions }`), returning a chosen `action_index` over the line protocol while the host brain builds and proves the R2 turn receipt.

#### `nanodregg/sandbox`
In [`/Users/ember/dev/nanodregg/sandbox/src/lib.rs`](file:///Users/ember/dev/nanodregg/sandbox/src/lib.rs#L1-L380), [`connect.rs`](file:///Users/ember/dev/nanodregg/sandbox/src/connect.rs#L1-L142), and [`custody.rs`](file:///Users/ember/dev/nanodregg/sandbox/src/custody.rs#L1-L195) (commits `af3dfd3` through `1ab410e`, Oct 2026):
- [`Policy`](file:///Users/ember/dev/nanodregg/sandbox/src/lib.rs#L65-L77) specifies `{ read, write, exec, hidden, connect }`, enforcing `CONNECT_MAX = 2` Unix domain sockets (`connect.rs:14`).
- Before spawning, [`confine`](file:///Users/ember/dev/nanodregg/sandbox/src/lib.rs#L150-L260) canonicalizes all paths (`O_NOFOLLOW` where required), refuses any policy where a `read`/`write`/`exec` path overlaps a `hidden` path (`ConfineError::Exposed`), refuses any program binary not covered by `read` or `exec` (`ConfineError::ProgramOutside`, commit `6278ab8`), and validates every `connect` socket via [`connect::validate`](file:///Users/ember/dev/nanodregg/sandbox/src/connect.rs#L35-L120) (`S_IFSOCK`, mode `0600` or `0660`, owned by `euid`, ancestor chain verified via `custody::chain` StrictModes walk).
- [`die_with_parent()`](file:///Users/ember/dev/nanodregg/sandbox/src/lib.rs#L105-L142) (commit `1ab410e`, 2026-10-24) binds child lifetime to its parent via `rustix::process::set_parent_process_death_signal( Some(Signal::KILL))` on Linux (checking `getppid() != ppid` after registration to close the fork race) and a background `orphan-watch` thread polling `getppid()` on macOS.
- Enforces confinement via `/usr/bin/sandbox-exec` on macOS (emitting `(deny file-read* (subpath ...))` after `(allow ...)` so `hidden` overrides broader read grants) or `/usr/local/libexec/nd-bwrap` on Linux (`--unshare-all --unshare-user --disable-userns --cap-drop ALL --new-session --die-with-parent`, binding an empty `0400` tmpfs over `hidden` directories and `/dev/null` over `hidden` files).

---

## 5. Object-Capability & Post-Quantum Credential Stack (`macaroon`, `token`, `dregg-auth`, `credentials`, `dregg-pq`, `pqvrf`, `intent`, `starbridge-apps`)

### 5.1 HMAC-SHA256 Macaroons (`macaroon`, `em2_`) & Third-Party Caveat Discharge

In [`macaroon/src/macaroon.rs`](file:///Users/ember/dev/breadstuffs/macaroon/src/macaroon.rs#L1-L260) and [`macaroon/src/caveat_3p.rs`](file:///Users/ember/dev/breadstuffs/macaroon/src/caveat_3p.rs#L1-L240):
- **HMAC-SHA256 Tag Chain**: Given `root_key: [u8; 32]` and random `nonce: [u8; 16]`:
  $$T_0 = \text{HMAC-SHA256}(\text{root\_key},\;\text{nonce}), \qquad T_i = \text{HMAC-SHA256}(T_{i-1},\;\text{encode}(C_i))$$
  Anyone holding the macaroon can append a caveat $C_{n+1}$ and replace $T_n$ with $T_{n+1} = \text{HMAC-SHA256}(T_n, \text{encode}(C_{n+1}))$ without knowing `root_key`; truncating $C_{n+1}$ requires inverting HMAC-SHA256 to recover $T_n$. Signature comparison uses `subtle::ConstantTimeEq`.
- **Third-Party Caveats (`ThirdPartyCaveat`)**:
  - [`add_third_party_caveat`](file:///Users/ember/dev/breadstuffs/macaroon/src/caveat_3p.rs#L80-L125) generates a random 32-byte caveat root key $r$, encrypts $r$ under the current HMAC tail $T_{i-1}$ using XChaCha20-Poly1305 (`verifier_key = seal(T_{i-1}, r)`), and encrypts `{r, caveats}` under the 3P service's shared key (`ticket = seal(shared_key, WireTicket { discharge_key: r, caveats })`, `#[derive(Zeroize, ZeroizeOnDrop)]`).
  - [`bind_discharge`](file:///Users/ember/dev/breadstuffs/macaroon/src/caveat_3p.rs#L150-L162) binds the discharge macaroon to the authorizing root macaroon by appending caveat ID `CAV_BIND_TO_PARENT (0xFE)` containing $\text{SHA-256}(T_{\text{root}})$.
  - [`verify_discharge`](file:///Users/ember/dev/breadstuffs/macaroon/src/caveat_3p.rs#L170-L235) is fail-closed: it enforces a 300-second freshness window (`MAX_DISCHARGE_AGE = 300`) and rejects any discharge macaroon that lacks a `CAV_BIND_TO_PARENT` caveat matching $\text{SHA-256}(T_{\text{root}})$, preventing cross-macaroon discharge replay.
- **Lean 4 Proofs ([`Dregg2/Authority/Caveat.lean`](file:///Users/ember/dev/breadstuffs/metatheory/Dregg2/Authority/Caveat.lean#L1-L210) & [`MacaroonDischarge.lean`](file:///Users/ember/dev/breadstuffs/metatheory/Dregg2/Authority/MacaroonDischarge.lean#L1-L220))**:
  - `theorem attenuate_narrows`, `theorem attenuate_subset`, `theorem macaroon_not_crossvat`, `theorem biscuit_crossvat` (`Caveat.lean:95-190`).
  - `theorem bound_discharge_verifies`, `theorem unbound_discharge_rejected`, `theorem binding_not_replayable_to_other_root`, `theorem rebinding_changes_replay` (`MacaroonDischarge.lean:115-198`).

---

### 5.2 Unified Token Layer (`token`: `em2_` & `eb2_`) and Hybrid Revocation (`RevocationRegistry`)

In [`token/src/lib.rs`](file:///Users/ember/dev/breadstuffs/token/src/lib.rs#L1-L150), [`token/src/biscuit_backend.rs`](file:///Users/ember/dev/breadstuffs/token/src/biscuit_backend.rs#L1-L240), and [`token/src/revocation.rs`](file:///Users/ember/dev/breadstuffs/token/src/revocation.rs#L1-L380):
- Unifies `em2_` (msgpack + URL-safe Base64 `MacaroonToken`) and `eb2_` (Ed25519 + Datalog `BiscuitToken` via `biscuit-auth` v6.0) behind the [`AuthToken`](file:///Users/ember/dev/breadstuffs/token/src/lib.rs#L55-L95) trait.
- **Revocation Non-Membership & Hybrid Root Attestation (`revocation.rs`)**:
  - [`SortedRevocationTree`](file:///Users/ember/dev/breadstuffs/token/src/revocation.rs#L110-L240) maintains revoked token hashes in sorted order in a BLAKE3 Merkle tree and produces a [`NonMembershipProof`](file:///Users/ember/dev/breadstuffs/token/src/revocation.rs#L155-L170) consisting of two adjacent leaves $(L_i, L_{i+1})$ with $L_i < x < L_{i+1}$ and their Merkle inclusion proofs, proving $x$ is not in the revoked set.
  - [`AttestedRevocationRoot`](file:///Users/ember/dev/breadstuffs/token/src/revocation.rs#L270-L355) signs the revocation root with both **Ed25519** and **ML-DSA-65** (`pq_signature: Option<Vec<u8>>`). [`AttestedRevocationRoot::verify_hybrid(&self, authority: &HybridAuthorityKey)`](file:///Users/ember/dev/breadstuffs/token/src/revocation.rs#L325-L352) requires **both** the classical Ed25519 signature and the post-quantum ML-DSA-65 signature (domain `"dregg-revocation-root-v1"`) to verify, failing closed if `pq_signature` is `None`.

---

### 5.3 Standalone Hybrid Post-Quantum Credentials (`dregg-auth`: `dga1_` / `dgd1_` & `eb2_`)

Introduced on 2026-06-09 (`3e4bfa483`) and upgraded to hybrid post-quantum in [`dregg-auth/src/credential/`](file:///Users/ember/dev/breadstuffs/dregg-auth/src/credential/mod.rs#L1-L652), `dregg-auth` implements an offline-attenuable, chain-independent capability credential (`dga1_` URL-safe Base64 token wire, `dgd1_` detached proof-of-possession signature wire):

- **Cryptographic Chain Structure ([`credential/chain.rs`](file:///Users/ember/dev/breadstuffs/dregg-auth/src/credential/chain.rs#L1-L165))**:
  - Each [`Block`](file:///Users/ember/dev/breadstuffs/dregg-auth/src/credential/chain.rs#L21-L39) contains:
    ```rust
    pub struct Block {
        pub caveats: Vec<Pred>,
        pub next_pub: VerifyingKey,
        pub next_pub_ml_dsa: Option<Box<MlDsaPubBytes>>, // 1952-byte ML-DSA-65 PK
        pub sig: Signature,                              // 64-byte Ed25519 sig
        pub sig_ml_dsa: Option<Box<MlDsaSigBytes>>,      // 3309-byte ML-DSA-65 sig
    }
    ```
  - A [`Credential`](file:///Users/ember/dev/breadstuffs/dregg-auth/src/credential/mod.rs#L168-L185) carries `root_pub: VerifyingKey`, `root_pub_ml_dsa: Option<Box<MlDsaPubBytes>>`, `blocks: Vec<Block>`, and the bearer tail secret `tail: SigningKey` (zeroized on drop, plus a cached `tail_ml_dsa_memo: Option<Arc<MlDsaSeedMemo>>` so repeated PQ operations do not re-run the ~200ms Lean ML-DSA keygen).
- **Hybrid Verification & DoS-Resistant Ordering ([`Credential::verify_hybrid`](file:///Users/ember/dev/breadstuffs/dregg-auth/src/credential/mod.rs#L406-L520))**:
  1. Checks `blocks.len() <= MAX_BLOCKS (32)` and total AST nodes `<= MAX_PRED_NODES (256)`.
  2. **Step 1 — Classical Proof-of-Possession (`check_pop_classical`)**: Fast (~50 µs) Ed25519 signature check against `last.next_pub` *before* touching any post-quantum verification.
  3. **Step 2 — Classical + PQ Chain Verification**: Pins `expected_key = root.ed25519` and `expected_pq = root.ml_dsa_65` from the enrolled [`HybridRootPublic`](file:///Users/ember/dev/breadstuffs/dregg-auth/src/credential/pq.rs#L35-L45) (never trusting the wire's self-reported `root_pub_ml_dsa`!). For every block $i$, verifies **both** `expected_key.verify_strict(&msg, &block.sig)` and `pq::ml_dsa_verify(&expected_pq, &msg, &block.sig_ml_dsa)` (under FIPS 204 context `CRED_PQ_CTX = b"dregg-auth v1 credential mldsa"`). Rejects with `VerifyError::MissingPostQuantumSignature { block: i }` if any block omits its ML-DSA-65 signature or key.
  4. **Step 3 — Post-Quantum Proof-of-Possession (`check_pop_pq`)**: Executed *after* chain authentication (`mod.rs:483-508`) so an unauthenticated attacker cannot force the verifier to derive a 1,952-byte ML-DSA-65 public key (~200 ms in Lean) on a forged token.
  5. **Step 4 — Fail-Closed 3-Valued Caveat Algebra ([`credential/pred.rs`](file:///Users/ember/dev/breadstuffs/dregg-auth/src/credential/pred.rs#L1-L220))**: Evaluates every `Pred` across all blocks using 3-valued logic (`Outcome::{Pass, Fail, Unbound}`). If a clock or attribute is absent from `Context`, comparison predicates return `Unbound`, and `Pred::Not(Unbound)` remains `Unbound` (which fails closed at top level), so `Not(AttrEq("role", "guest"))` can **never** invert a missing `"role"` attribute into a pass!
- **Lean 4 Proofs ([`Dregg2/Authority/Biscuit.lean`](file:///Users/ember/dev/breadstuffs/metatheory/Dregg2/Authority/Biscuit.lean) & [`BiscuitGraph.lean`](file:///Users/ember/dev/breadstuffs/metatheory/Dregg2/Authority/BiscuitGraph.lean))**:
  - `theorem biscuit_narrows`, `theorem amplifying_block_rejected`, `theorem forged_block_rejected`, `theorem sealed_biscuit_final`.

---

### 5.4 Lean-Verified Post-Quantum Cryptography (`dregg-pq` & `pqvrf`)

#### `dregg-pq`: `leanc`-Compiled FIPS 204 (ML-DSA-65) & FIPS 203 (ML-KEM-768) with Uncatchable Audit Gate
Consolidated on 2026-07-09 (commits `13eff7a3f`, `7aa833047`, `0cdfd2ed5`, `8f5d51acf`, `f52d8ed91`), [`dregg-pq/src/lib.rs`](file:///Users/ember/dev/breadstuffs/dregg-pq/src/lib.rs#L1-L165) is the workspace's single post-quantum leaf crate:
- **ML-DSA-65 (`dregg-pq/src/mldsa.rs`)**: Parameter set ML-DSA-65 (FIPS 204, NIST Security Category 3): `PK_LEN = 1952`, `SK_LEN = 4032`, `SIG_LEN = 3309`.
- **Hybrid X25519 + ML-KEM-768 (`dregg-pq/src/hybrid_kem.rs`)**: Parameter set ML-KEM-768 (FIPS 203): `EK_LEN = 1184`, `DK_LEN = 2400`, `CT_LEN = 1088`. [`hybrid_kem::combine`](file:///Users/ember/dev/breadstuffs/dregg-pq/src/hybrid_kem.rs#L112-L135) implements the X-Wing / IETF hybrid KEM combiner (`DOMAIN = b"dregg-hybrid-kem-x25519-mlkem768-v1"`):
  $$\text{ikm} = \text{ss}_{\text{X25519}} \mathbin{\Vert} \text{ss}_{\text{ML-KEM-768}}, \qquad K = \text{HKDF-SHA256}(\text{salt} = \text{DOMAIN},\;\text{ikm},\;\text{info} = \text{DOMAIN} \mathbin{\Vert} \text{transcript})$$
  Remaining secure if *either* X25519 (IND-CCA under Gap-CDH) *or* ML-KEM-768 (IND-CCA under Module-LWE) holds.
- **Lean-Verified Core Hook Table (`PqSite` & `dregg-exec-lean`)**:
  All 6 post-quantum operations ([`PqSite::ALL`](file:///Users/ember/dev/breadstuffs/dregg-pq/src/audit.rs#L45-L62): `MlDsaVerify`, `MlDsaSign`, `MlDsaKeygen`, `MlKemEncaps`, `MlKemDecaps`, `MlKemKeygen`) dispatch through `OnceLock` hooks populated by `dregg_exec_lean::register_lean_fips204_verify()`, which links the `leanc`-compiled Lean 4 implementations (`dregg_fips204_verify_real`, `dregg_fips204_sign_real`, `dregg_mldsa_keygen_real`, `dregg_mlkem_keygen_real`, `dregg_mlkem_encaps_real`, `dregg_mlkem_decaps_real`).
- **Uncatchable Fail-Closed Audit Gate ([`dregg-pq/src/audit.rs`](file:///Users/ember/dev/breadstuffs/dregg-pq/src/audit.rs#L120-L245))**:
  If any of the 6 PQ sites is invoked before its Lean-verified core is registered:
  - [`enter_unaudited`](file:///Users/ember/dev/breadstuffs/dregg-pq/src/audit.rs#L195-L245) writes a diagnostic banner directly to file descriptor 2 via `libc::write(2, ...)` (`eprintln_fd2`, bypassing Rust's buffered `std::io::stderr()` so the reason is never lost on abort) and calls **`std::process::abort()`** (`SIGABRT`, which cannot be caught by `std::panic::catch_unwind`).
  - Even if `DREGG_ALLOW_UNAUDITED_PQ=1` is set in the environment, setting `DREGG_REQUIRE_LEAN=1` revokes the override (`audit.rs:155-168`) and forces `std::process::abort()`.

#### `pqvrf`: Lattice-Based Post-Quantum VRF (`Dregg2.Crypto.VRF`)
Introduced in commit `19205169f` (2026-07-11), [`pqvrf/src/lib.rs`](file:///Users/ember/dev/breadstuffs/pqvrf/src/lib.rs#L1-L320) implements the Esgin, Kuchta, Sakzad, Steinfeld, Zhao, and Liu (FC 2021) Module-LWE / Module-SIS Lattice-Based VRF over the cyclotomic ring $R_q = \mathbb{Z}_q[X]/(X^d + 1)$:
- **Exact Set I Parameters ([`pqvrf/src/lib.rs:62-92`](file:///Users/ember/dev/breadstuffs/pqvrf/src/lib.rs#L62-L92))**:
  - Ring degree $d = 256$ (`DEGREE = 256`)
  - Primary modulus $q = 100,679,681$ (`MODULUS_Q`, 27-bit prime, $q \equiv 1 \pmod{512}$)
  - Rounding modulus $p = 2,097,169$ (`MODULUS_P`, 21-bit)
  - Module-SIS rank $k = 4$ (`MSIS_RANK = 4`), secret width $l = 9$ (`SECRET_WIDTH = 9`)
  - Ternary challenge weight $\kappa = 39$ (`CHALLENGE_WEIGHT = 39`, $\approx 2^{192}$ challenge space)
  - Rejection-sampling mask bound $\gamma = 89,856$ (`MASK_BOUND`), norm bound $\beta = \gamma - \kappa = 89,817$ (`NORM_BOUND`).
- **Lean 4 Uniqueness Theorem ([`metatheory/Dregg2/Crypto/VRF.lean`](file:///Users/ember/dev/breadstuffs/metatheory/Dregg2/Crypto/VRF.lean))**: `theorem lattice_vrf_uniqueness_reduces_to_msis` proves that any two valid proofs $(\pi_1, \pi_2)$ for the same public key and input yielding distinct VRF outputs produce a short non-zero vector $z = s_1 - s_2$ solving $\text{MSIS}_{q, k, l, 2\beta}$.

---

### 5.5 Anonymous Selective-Disclosure Credentials (`credentials`)

In [`credentials/src/lib.rs`](file:///Users/ember/dev/breadstuffs/credentials/src/lib.rs#L1-L150), [`issuance.rs`](file:///Users/ember/dev/breadstuffs/credentials/src/issuance.rs), [`presentation.rs`](file:///Users/ember/dev/breadstuffs/credentials/src/presentation.rs), [`verification.rs`](file:///Users/ember/dev/breadstuffs/credentials/src/verification.rs#L1-L260), and [`revocation.rs`](file:///Users/ember/dev/breadstuffs/credentials/src/revocation.rs):
- **Blinded Issuer Federation & Selective Disclosure**:
  - [`issue`](file:///Users/ember/dev/breadstuffs/credentials/src/issuance.rs) mints a `Credential` backed by an Ed25519 + Datalog Biscuit token (`attr("cred_type", ...)`, `attr(field, value)`, `attr("subject_commitment", hex(BLAKE3("dregg-credential-subject-v1" || holder_secret || issuer_pubkey)))`) and registers the issuer's public key in a blinded Poseidon2 Merkle federation registry (`BlindedFederationRegistry`).
  - [`present_anonymous`](file:///Users/ember/dev/breadstuffs/credentials/src/presentation.rs) produces an unlinkable `Presentation` using a per-presentation `presentation_nonce` (`rerandomized_leaf = Poseidon2(issuer_leaf, nonce)`) so multiple presentations of the same credential cannot be correlated (`unlinkable multi-show`), while optionally attaching `Gte`/`Lte`/`InRange` predicate proofs (`CredentialPredicate`) and a non-membership [`RevocationProof`](file:///Users/ember/dev/breadstuffs/credentials/src/revocation.rs) against the revocation tree.
- **Injective 9-Lane Base-$2^{28}$ Field Encoding (`field_limbs9`)**:
  - In [`credentials/src/verification.rs`](file:///Users/ember/dev/breadstuffs/credentials/src/verification.rs#L45-L95), `compute_revealed_terms_commitment` hashes revealed attributes using domain `"dregg-credentials-revealed-v2"` and encodes each 256-bit digest into **9 base-$2^{28}$ BabyBear limbs** (`field_limbs9`, $9 \times 28 = 252 \ge 248$ bits), proved injective in Lean (`Dregg2.Circuit.FieldLanes9.fieldToLanes9_injective`), replacing an older non-injective `from_le_bytes % P` reduction.
- **Fail-Closed Verification & Residual-Gap Honesty (`verification.rs:140-215`)**:
  - [`verify`](file:///Users/ember/dev/breadstuffs/credentials/src/verification.rs#L115-L235) requires `expected_federation_root == proof.federation_root`, checks expiration, verifies `RevocationProof`, checks `revealed_terms_commitment`, and **fail-closes** on `expected_predicates` (`VerificationError::PredicateProofInvalid`), documenting in-code that until the emitted predicate AIR binds `facts_root` as a public input, predicate-bearing credential presentations are refused rather than silently accepted.

---

### 5.6 Agent Mandates, Audit Proofs, & Verifiable MCP Delegation (`intent`, `audit`, `starbridge-apps`)

*(Note: A repository-wide and `cv --frozen` search confirms there is no type literally named `AlignmentProof`; agent alignment, mandate containment, and usage auditing are implemented via `intent::agent_mandate::Mandate` / `DelegTree`, `audit::proofs::{CountProof, RangeProof, LastUseProof, ConsistencyProof, BudgetProof}`, and the Lean-verified `starbridge-apps` `agent-provenance` and `tool-access-delegation`.)*

#### `intent/src/agent_mandate.rs` & Lean `Dregg2.Agent.Mandate`
In [`intent/src/agent_mandate.rs`](file:///Users/ember/dev/breadstuffs/intent/src/agent_mandate.rs#L1-L512) and [`metatheory/Dregg2/Agent/Mandate.lean`](file:///Users/ember/dev/breadstuffs/metatheory/Dregg2/Agent/Mandate.lean#L1-L320):
- [`Mandate::sub_delegate`](file:///Users/ember/dev/breadstuffs/intent/src/agent_mandate.rs#L150-L167) constructs a child mandate whose `target` is fixed to `self.target`, whose rights are intersected (`&self.keep & want`), whose `budget` is clamped (`ask_budget.min(self.budget)`), and whose `caveat` is intersected (`self.caveat.intersect(extra_caveat)`).
- [`DelegTree`](file:///Users/ember/dev/breadstuffs/intent/src/agent_mandate.rs#L214-L324) enforces:
  - `well_attenuated`: every child's rights, budget, target, and caveat narrow its parent's.
  - `no_amplify`: every node in the tree satisfies `m.keep.is_subset(&root.keep)`.
  - `budget_bounded`: every node satisfies `m.budget <= root.budget`.
  - `budget_partitioned`: at every internal node, $\sum_{c \in \text{children}} c.\text{budget} \le \text{node}.\text{budget}$ (conservation of delegated budget across parallel sub-agents).
  - `materialize_grants()` → `Vec<Effect::GrantCapability>` and `materialize_revoke(child)` → `Effect::RevokeDelegation { child }`.
- **Lean 4 Theorems ([`Dregg2/Agent/Mandate.lean`](file:///Users/ember/dev/breadstuffs/metatheory/Dregg2/Agent/Mandate.lean#L120-L310))**:
  - `theorem subtree_rights_le_root`:
    ```lean
    theorem subtree_rights_le_root (t : DelegTree) ( probe : List MethodId)
        (hw : wellAttenuated probe t = true) :
        ∀ m ∈ mandateList t, ∀ a, a ∈ m.keep → a ∈ (rootMandate t).keep
    ```
  - `theorem materialize_non_amplifying`, `theorem children_no_oversubscribe`, `theorem subtree_budget_le_root`, and `theorem revoke_kills_subtree`.

#### `starbridge-apps/agent-provenance` & Lean `Dregg2.Apps.AgentProvenanceGated`
In [`starbridge-apps/agent-provenance/src/lib.rs`](file:///Users/ember/dev/breadstuffs/starbridge-apps/agent-provenance/src/lib.rs#L1-L320) and [`metatheory/Dregg2/Apps/AgentProvenanceGated.lean`](file:///Users/ember/dev/breadstuffs/metatheory/Dregg2/Apps/AgentProvenanceGated.lean#L1-L401):
- The provenance cell configures `HEAD_SLOT = 2` (`"head"`) with `SlotCaveat::Monotonic`, `TIP_SLOT = 3` (`"tip"`), and `ENTRY_BASE + i` (`"entry0"`, `"entry1"`, ...) each with `SlotCaveat::WriteOnce`.
- Each entry stores `link_hash(prev, claim) = BLAKE3("dregg-provenance-link\x01" || prev || claim)` (with [`IncrementalChainVerifier`](file:///Users/ember/dev/breadstuffs/starbridge-apps/agent-provenance/src/lib.rs#L240-L295) maintaining $O(1)$ incremental verification state).
- **Lean 4 Theorems ([`AgentProvenanceGated.lean:154-309`](file:///Users/ember/dev/breadstuffs/metatheory/Dregg2/Apps/AgentProvenanceGated.lean#L154-L309), all `#assert_axioms`-clean)**:
  - `theorem prov_forged_credential_rejected (s : RecChainedState) (slot : FieldName) (value : Int) : execFullForestG s (provNode forgedCred slot value) = none`
  - `theorem prov_entry_writeonce (s : RecChainedState) (i : Nat) (digest : Int) (hgate : gateOK (mkAuth goodCred []) s = true) (hfrozen : caveatsAdmit s.kernel (entrySlot i) agentActor logCell digest = false) : execFullForestG s (appendEntryRaw goodCred i digest) = none`
  - `theorem prov_head_cannot_rewind (s : RecChainedState) (newHead : Int) (hgate : gateOK (mkAuth goodCred []) s = true) (hrewind : caveatsAdmit s.kernel headSlot agentActor logCell newHead = false) : execFullForestG s (advanceHeadNode goodCred newHead) = none`
  - `theorem prov_append_reads_back`, `theorem prov_append_audited`, `theorem prov_chain_links`, `theorem prov_chain_tamper_rejected`, `theorem prov_append_conserves`.

#### `starbridge-apps/tool-access-delegation` & Lean `Dregg2.Apps.ToolAccessDelegation`
In [`starbridge-apps/tool-access-delegation/src/lib.rs`](file:///Users/ember/dev/breadstuffs/starbridge-apps/tool-access-delegation/src/lib.rs#L1-L310) and [`metatheory/Dregg2/Apps/ToolAccessDelegation.lean`](file:///Users/ember/dev/breadstuffs/metatheory/Dregg2/Apps/ToolAccessDelegation.lean#L1-L478):
- Mints a mandate cell with `CALLS_MADE_SLOT = 0` (`Monotonic` + `FieldLteField { target_slot: 1 }`), `RATE_LIMIT_SLOT = 1` (`WriteOnce`), `DEADLINE_SLOT = 2` (`WriteOnce` + `FieldGteHeight`), and `TOOL_ID_SLOT = 3` (`WriteOnce`).
- [`deleg_admit`](file:///Users/ember/dev/breadstuffs/starbridge-apps/tool-access-delegation/src/lib.rs#L160-L185) calls the `@[export dregg_deleg_admit]` Lean function `Dregg2.Apps.DelegAdmit.delegAdmit` directly across `dregg-lean-ffi`.
- **Lean 4 Headline Theorem ([`ToolAccessDelegation.lean:179-193`](file:///Users/ember/dev/breadstuffs/metatheory/Dregg2/Apps/ToolAccessDelegation.lean#L179-L193), `#assert_axioms`-clean)**:
  ```lean
  theorem tool_invocation_commit_iff_admit (g : Grant) (now tool : Int) (cell worker : CellId)
      (s : RecChainedState) (c : Int)
      (hprog : s.kernel.slotCaveats cell = (mandateSpec g now tool cell).caveats)
      (hcur : (mandateSpec g now tool cell).committed s.kernel = c)
      (hold : c ∈ (mandateSpec g now tool cell).oldRange)
      (hnew : (c + 1) ∈ (mandateSpec g now tool cell).newRange) :
      (execFullA s (.setFieldA worker cell callsMadeSlot (c + 1))).isSome = true
        ↔ (delegAdmit g now tool c (c + 1) = true
            ∧ (stateStep s callsMadeSlot worker cell (.int (c + 1))).isSome = true)
  ```
  Plus the rejection teeth `tool_invocation_over_rate_rejected`, `tool_invocation_past_deadline_rejected`, `tool_invocation_out_of_scope_rejected`, `invocation_forged_rejected`, `invocation_revoked_rejected`, and kernel keystones `tool_invocation_conserves` and `tool_invocation_no_amplify`.

---

## 6. Chronological Git & `cv` Archaeology

### Phase 1: `~/elide/oauth` → `~/elide/breadstuffs` (2026-02-07, Session `95e87c6f-fb60-4963-a126-0b26186708ad`)
The entire capability lineage began on **2026-02-07** inside `~/elide/oauth`, which Ember renamed to `~/elide/breadstuffs` in Claude Code session `95e87c6f-fb60-4963-a126-0b26186708ad` (recorded in [`/Users/ember/.claude/history.jsonl`](file:///Users/ember/.claude/history.jsonl) and [`/Users/ember/.claude/projects/-Users-ember-elide-breadstuffs/memory/MEMORY.md`](file:///Users/ember/.claude/projects/-Users-ember-elide-breadstuffs/memory/MEMORY.md#L1-L54)):

- **1770467854240 (2026-02-07)**:
  > `"(we just renamed this from ~/elide/oauth to ~/elide/breadstuffs, ensure any path references in .git get fixed, idk if there even are any)"`
- **1770467968194 (2026-02-07)**:
  > `"Excellent! Now, you can read docs/ for more about what we are up to on this branch. We are working on \"breadstuffs,\" excellent implementations of macaroons and biscuits to offer to our runtime customers. We also want to offer value-provided cloud services that complement this, as a monetization strategy for our company, so we can make open source for the whole planet and still eat meals in a home. We need to make a huge design effort."`
- **1770468126947 (2026-02-07)**:
  > `"Cloud services and improving the actual interface and proving out its real-world utility with awesome, \"killer app\" style demos. (we don't want to extract breadstuffs into its own product, it is firmly a component of elide. but the crates, well, we can easily package it up later whenever we want). We basically want to weaponize biscuits and macaroons."`

In that February 2026 sprint ([`weaponize-progress.md`](file:///Users/ember/.claude/projects/-Users-ember-elide-breadstuffs/memory/weaponize-progress.md#L1-L72), [`security-fixes.md`](file:///Users/ember/.claude/projects/-Users-ember-elide-breadstuffs/memory/security-fixes.md#L1-L37)), Ember built the `em2_` HMAC-SHA256 `macaroon` crate (with XChaCha20-Poly1305 3P caveats and `ZeroizeOnDrop` `WireTicket`s), the `eb2_` Ed25519 + Datalog `token` crate (`FeatureGlob`, `Budget`, `Revocable`), and the cuckoo-filter revocation mesh.

### Phase 2: `pyana` — Distributed Object-Capability Runtime with ZK Proofs (2026-05-19..21)
After leaving Elide, Ember extracted the `macaroon` and `token` crates into `/Users/ember/dev/breadstuffs` as **`pyana`**:
- **`3d0d0bfafb2d89fef4ed03537b5191f85dbc1cf5` (2026-05-19)**: *"pyana: distributed object-capability authorization with ZK proofs — A post-quantum capable authorization system for AI agent execution across trust domains. Prove you're authorized without revealing your delegation chain. 22 crates, ~70k LOC, 1000+ tests."* (Importing `macaroon`, `token`, `cell`, `bridge`, `audit`, `circuit`).
- **`d5be7258e` (2026-05-20)**: Added the distributed `intent` engine (`Intent`, `MatchSpec`, `Fulfillment`).
- **`77b998170` / `d1b48d885` (2026-05-24)**: Added the `credentials` crate (selective disclosure, blinded federation registry, unlinkable multi-show).

### Phase 3: Standalone Agent Auth, Bare-Metal `seL4`, & Lean-Verified PQ (`dregg`, June–July 2026)
- **`3e4bfa483` (2026-06-09) & `d15b94f63` (2026-06-11)**: Created `dregg-auth` (`dga1_` / `eb2_` offline-attenuable agent permission wedge and MCP gateway profile).
- **`8ef312b5e`, `a744edfc0`, `2490e7f33`, `f49b87b35` (2026-06-13) & `7cb8626a41` (2026-06-15)**: Built the `sel4/` Microkit 2.2.0 6-PD system, `dregg-firmament` (`Capability` unifying seL4 CNode caps and distributed cell caps), and `verifier-stark` proving and verifying a 78,135-byte BabyBear + BLAKE3 + FRI STARK inside a bare-metal seL4 protection domain on ARM64 and RISC-V64.
- **`5a707ec02`, `44e272708`, `ab659504d` (2026-07-05..06)**: Built `grain-jail` (`ConfinedBrain` + macOS Seatbelt / Linux Landlock+seccomp-BPF process confinement).
- **`13eff7a3f`, `7aa833047`, `0cdfd2ed5`, `8f5d51acf`, `f52d8ed91` (2026-07-09)**: Consolidated all post-quantum cryptography into `dregg-pq`, routing ML-DSA-65 (FIPS 204) and ML-KEM-768 (FIPS 203) through `leanc`-compiled Lean-verified cores with the uncatchable `std::process::abort()` audit gate (`audit.rs`).
- **`19205169f` (2026-07-11)**: Built `pqvrf` (Esgin et al. FC 2021 Module-LWE / Module-SIS lattice VRF bound to Lean `Dregg2.Crypto.VRF.lattice_vrf_uniqueness_reduces_to_msis`).

### Phase 4: Hardware TEE Roots of Trust, Confidential GPU E2EE, & Residual Trust Proofs (July–October 2026)
- **`17b6e5539` & `8ce36ba16` (2026-07-11), `ad33c9247` (2026-07-12), `261a06f8d` (2026-07-13)**: Built `tee-verify` (`NitroVerifier`, `SnpVerifier` with Milan/Genoa/Turin RSA-4096 PSS ARK→ASK→VCEK chains, `TdxVerifier`) and `tee-produce` (`NitroNsmBackend` over `/dev/nsm`).
- **`9d5d06853` (2026-07-23), `6f38efbe3` (2026-07-26), `4bcb934a3` (2026-07-27)**: Built `dregg-chutes-e2ee` (confidential GPU TDX attestation + ML-KEM-768 / HKDF-SHA256 / ChaCha20-Poly1305 E2EE) and `attest-check` (`dungeon-attest-check` 6-link provenance verifier).
- **`ac77a4d` (2026-08-18)**: Proved in `degg-research` (`experiments/shielded-baseline/tests/residual_trust.rs`, Verdicts V3/V4) that an unproved TEE/shielded matcher can forge **377 out of 1,125** clearing outcomes (`33/33` headers) that pass every participant's local fill audit.
- **`4d98292c2`, `a9d5df4db`, `551fc897f`, `3bf5e041a`, `3ecfd0bd1`, `292829518` (2026-09-30)**: Closed the 2026-07-25 TEE and Firmament security audit findings (`F1`–`F3`, `F10`–`F14`).
- **`af3dfd3`..`1ab410e` (2026-10-16..24)**: Built `nanodregg/sandbox` (deny-by-default macOS `sandbox-exec` and Linux `nd-bwrap` confinement, `custody` StrictModes directory walk, `CONNECT_MAX = 2` socket validation, and `die_with_parent`).
