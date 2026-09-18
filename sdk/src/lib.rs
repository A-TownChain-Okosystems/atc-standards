//! ATC Standards SDK — typed access to the canonical standards registry.
use serde::{Deserialize, Serialize};
#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
pub struct StandardRef { pub id: String, pub version: String, pub status: String }
#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
pub struct ConformanceResult { pub standard_id: String, pub compliant: bool, pub findings: Vec<String> }
pub fn standard_ref(id: impl Into<String>, version: impl Into<String>, status: impl Into<String>) -> StandardRef {
    StandardRef { id: id.into(), version: version.into(), status: status.into() }
}
pub fn conformance(id: impl Into<String>, compliant: bool, findings: Vec<String>) -> ConformanceResult {
    ConformanceResult { standard_id: id.into(), compliant, findings }
}
#[cfg(test)] mod tests { use super::*; #[test] fn creates_ref(){ assert_eq!(standard_ref("ATC-STD-000","1.0.0","STABLE").id,"ATC-STD-000"); } }
