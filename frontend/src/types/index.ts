export interface User {
  id: string;
  email: string;
  full_name: string;
  date_of_birth?: string;
  biological_sex?: string;
  created_at: string;
}

export interface AuthState {
  user: User | null;
  token: string | null;
  isAuthenticated: boolean;
}

export interface AnatomicalLocation {
  id: string;
  name: string;
  system: 'HEAD' | 'CHEST' | 'ABDOMEN' | 'SPINE' | 'EXTREMITIES' | 'GENERAL';
  description: string;
}

export interface SymptomDefinition {
  id: string;
  name: string;
  system: 'NEUROLOGICAL' | 'RESPIRATORY' | 'DIGESTIVE' | 'MUSCULOSKELETAL' | 'GENERAL';
  description: string;
  synonyms: string[];
  allowed_locations: string[];
  primary_fact_name?: string;
  severity_options: string[];
  duration_options: string[];
  character_options: string[];
  common_triggers: string[];
  is_emergency_candidate: boolean;
}

export interface SymptomCatalogResponse {
  total_symptoms: number;
  systems: string[];
  symptoms: SymptomDefinition[];
  anatomical_locations: AnatomicalLocation[];
}

export interface ParseSymptomsResponse {
  extracted_symptom_ids: string[];
  extracted_location_ids: string[];
  duration?: string | null;
  severity?: string | null;
  character?: string | null;
  negated_facts: string[];
  confidence: number;
  ambiguous_details: string[];
  source?: string;
}

export interface QuestionOption {
  id: string;
  label: string;
  fact_value: string;
  is_red_flag?: boolean;
}

export interface AdaptiveQuestion {
  id: string;
  prompt: string;
  subtext?: string;
  target_fact_name: string;
  answer_type: 'BOOLEAN' | 'SINGLE_CHOICE' | 'MULTI_CHOICE' | 'SEVERITY_SCALE' | 'FREE_TEXT';
  options: QuestionOption[];
  associated_symptoms: string[];
  priority: number;
  is_safety_critical: boolean;
  evidence_provenance?: string;
}

export interface AdaptiveQuestionResponse {
  has_more_questions: boolean;
  question?: AdaptiveQuestion | null;
  answered_count: number;
  emergency_detected: boolean;
  emergency_message?: string;
}

export interface AssessmentConclusion {
  id: string;
  rule_id: string;
  category: string;
  summary: string;
  detailed_explanation?: string;
  recommendation_tier: 'EMERGENCY' | 'URGENT_EVALUATION' | 'CONSULT_PHYSICIAN' | 'SELF_MONITOR' | 'ROUTINE_PREVENTIVE';
  confidence: number;
  actionable_steps?: string[];
}

export interface AssessmentSummary {
  id: string;
  primary_complaint: string;
  status: string;
  current_step?: string;
  recommendation_tier?: string;
  emergency_flagged?: boolean;
  top_conclusion?: string;
  created_at: string;
}

export interface AssessmentDetail {
  id: string;
  user_id: string;
  status: string;
  current_step: string;
  primary_complaint: string;
  reported_symptoms_json: string[];
  selected_locations_json: string[];
  properties_json: Record<string, any>;
  gemini_narrative?: string;
  recommendation_tier?: string;
  created_at: string;
  conclusions: AssessmentConclusion[];
  trace?: any;
}

export interface TimelineObservation {
  id: string;
  user_id: string;
  assessment_id?: string;
  title: string;
  notes?: string;
  severity: 'MILD' | 'MODERATE' | 'SEVERE' | 'CRITICAL';
  recorded_at: string;
}

export interface ReportItem {
  id: string;
  assessment_id: string;
  title: string;
  checksum_sha256: string;
  created_at: string;
  report_data: Record<string, any>;
}

export interface GraphNodeData {
  label: string;
  sublabel?: string;
  node_type: 'FACT' | 'RULE' | 'CONCLUSION' | 'SAFETY' | 'MISSING_INFO';
  state: 'ACTIVE' | 'INACTIVE' | 'FIRED' | 'SKIPPED' | 'EMERGENCY' | 'CONFIRMED';
  metadata?: Record<string, any>;
  step?: number;
}

export interface GraphNode {
  id: string;
  type: string;
  position: { x: number; y: number };
  data: GraphNodeData;
}

export interface GraphEdge {
  id: string;
  source: string;
  target: string;
  type?: string;
  animated?: boolean;
  data?: {
    relationship: string;
    label?: string;
    step?: number;
  };
}

export interface GraphPayload {
  graph_id: string;
  assessment_id: string;
  kb_version: string;
  nodes: GraphNode[];
  edges: GraphEdge[];
  total_steps: number;
}
