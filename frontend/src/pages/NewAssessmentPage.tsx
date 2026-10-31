import React, { useState, useEffect } from 'react';
import { 
  Sparkles, 
  ArrowRight, 
  ArrowLeft, 
  ShieldAlert, 
  CheckCircle2, 
  Activity, 
  MapPin, 
  Gauge, 
  PhoneCall, 
  AlertTriangle,
  RotateCcw,
  Stethoscope
} from 'lucide-react';
import { api } from '../services/api';
import { 
  SymptomDefinition, 
  AnatomicalLocation, 
  ParseSymptomsResponse,
  AdaptiveQuestion 
} from '../types';
import { NaturalLanguageInput } from '../components/symptom-analyzer/NaturalLanguageInput';
import { SymptomTagSelector } from '../components/symptom-analyzer/SymptomTagSelector';
import { AnatomicalRegionSelector } from '../components/symptom-analyzer/AnatomicalRegionSelector';
import { SymptomPropertiesCard } from '../components/symptom-analyzer/SymptomPropertiesCard';
import { AdaptiveQuestionView } from '../components/symptom-analyzer/AdaptiveQuestionView';

type WizardStep = 'DESCRIBE' | 'UNDERSTAND' | 'CLARIFY' | 'ANALYZING';

export const NewAssessmentPage: React.FC<{ navigate: (route: string, param?: string) => void }> = ({ navigate }) => {
  const [currentStep, setCurrentStep] = useState<WizardStep>('DESCRIBE');
  
  // Catalog state
  const [catalogLoaded, setCatalogLoaded] = useState(false);
  const [symptoms, setSymptoms] = useState<SymptomDefinition[]>([]);
  const [locations, setLocations] = useState<AnatomicalLocation[]>([]);

  // Step 1: User Inputs
  const [freeText, setFreeText] = useState('Throbbing headache on my right temple for two days with nausea, but no fever.');
  const [isAnalyzingNLP, setIsAnalyzingNLP] = useState(false);
  const [nlpResult, setNlpResult] = useState<ParseSymptomsResponse | null>(null);
  
  const [selectedSymptomIds, setSelectedSymptomIds] = useState<string[]>(['sym_headache', 'sym_nausea']);
  const [selectedLocationIds, setSelectedLocationIds] = useState<string[]>(['loc_temple_right']);
  const [duration, setDuration] = useState('1-3 Days');
  const [severity, setSeverity] = useState('Moderate');
  const [character, setCharacter] = useState('Pulsating / Throbbing');

  // Step 3: Adaptive assessment state
  const [assessmentId, setAssessmentId] = useState<string | null>(null);
  const [currentQuestion, setCurrentQuestion] = useState<AdaptiveQuestion | null>(null);
  const [questionCount, setQuestionCount] = useState(1);
  const [answeredCount, setAnsweredCount] = useState(0);
  const [isSubmittingAnswer, setIsSubmittingAnswer] = useState(false);
  const [emergencyDetected, setEmergencyDetected] = useState(false);
  const [emergencyMessage, setEmergencyMessage] = useState<string>('');

  // Load catalog on mount
  useEffect(() => {
    api.getSymptomCatalog()
      .then((data) => {
        setSymptoms(data.symptoms);
        setLocations(data.anatomical_locations);
        setCatalogLoaded(true);
      })
      .catch((err) => {
        console.error('Failed to load symptom catalog:', err);
      });
  }, []);

  // Handlers for symptom and location selection
  const handleToggleSymptom = (id: string) => {
    setSelectedSymptomIds(prev => 
      prev.includes(id) ? prev.filter(x => x !== id) : [...prev, id]
    );
  };

  const handleToggleLocation = (id: string) => {
    setSelectedLocationIds(prev => 
      prev.includes(id) ? prev.filter(x => x !== id) : [...prev, id]
    );
  };

  // NLP Parse Trigger
  const handleAnalyzeNLP = async () => {
    if (!freeText.trim()) return;
    setIsAnalyzingNLP(true);
    try {
      const res = await api.parseSymptoms(freeText);
      setNlpResult(res);

      // Merge extracted symptoms
      if (res.extracted_symptom_ids && res.extracted_symptom_ids.length > 0) {
        setSelectedSymptomIds(prev => Array.from(new Set([...prev, ...res.extracted_symptom_ids])));
      }
      // Merge extracted locations
      if (res.extracted_location_ids && res.extracted_location_ids.length > 0) {
        setSelectedLocationIds(prev => Array.from(new Set([...prev, ...res.extracted_location_ids])));
      }
      if (res.duration) setDuration(res.duration);
      if (res.severity) setSeverity(res.severity);
      if (res.character) setCharacter(res.character);
    } catch (err) {
      console.error('NLP parse error:', err);
    } finally {
      setIsAnalyzingNLP(false);
    }
  };

  // Move from Step 1 to Step 2 (Understand)
  const handleProceedToUnderstand = () => {
    if (selectedSymptomIds.length === 0 && !freeText.trim()) {
      alert('Please describe your symptoms or select at least one symptom tag.');
      return;
    }
    setCurrentStep('UNDERSTAND');
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  // Move from Step 2 to Step 3 (Clarify: start backend assessment session)
  const handleStartClarifyingQuestions = async () => {
    try {
      setCurrentStep('CLARIFY');
      window.scrollTo({ top: 0, behavior: 'smooth' });

      const startRes = await api.startAssessment({
        primary_complaint: freeText.trim() || 'Structured Symptom Evaluation',
        symptom_ids: selectedSymptomIds,
        location_ids: selectedLocationIds,
        duration,
        severity,
        character
      });

      const aid = startRes.assessment_id;
      setAssessmentId(aid);

      // Fetch the first adaptive question
      const qRes = await api.getNextQuestion(aid);
      if (qRes.emergency_detected) {
        setEmergencyDetected(true);
        setEmergencyMessage(qRes.emergency_message || 'Emergency indicator detected.');
      } else if (qRes.has_more_questions && qRes.question) {
        setCurrentQuestion(qRes.question);
        setAnsweredCount(qRes.answered_count);
      } else {
        // No questions needed, proceed straight to completion
        handleCompleteAssessment(aid);
      }
    } catch (err) {
      console.error('Failed to start assessment:', err);
      alert('Could not start assessment session. Please check your connection.');
    }
  };

  // Submit answer for an adaptive question
  const handleSubmitAnswer = async (factName: string, value: string, rawResponse?: any) => {
    if (!assessmentId) return;
    setIsSubmittingAnswer(true);

    try {
      await api.submitAnswer(assessmentId, {
        question_id: currentQuestion?.id || 'q_adhoc',
        fact_name: factName,
        value,
        raw_response: rawResponse
      });

      // Query next question
      const nextQRes = await api.getNextQuestion(assessmentId);
      if (nextQRes.emergency_detected) {
        setEmergencyDetected(true);
        setEmergencyMessage(nextQRes.emergency_message || 'Emergency red flag detected.');
        setIsSubmittingAnswer(false);
        return;
      }

      if (nextQRes.has_more_questions && nextQRes.question) {
        setCurrentQuestion(nextQRes.question);
        setQuestionCount(prev => prev + 1);
        setAnsweredCount(nextQRes.answered_count);
      } else {
        // All adaptive questions answered
        await handleCompleteAssessment(assessmentId);
      }
    } catch (err) {
      console.error('Failed to submit answer:', err);
    } finally {
      setIsSubmittingAnswer(false);
    }
  };

  // Complete assessment and navigate to result
  const handleCompleteAssessment = async (aidToComplete?: string) => {
    const aid = aidToComplete || assessmentId;
    if (!aid) return;

    setCurrentStep('ANALYZING');
    window.scrollTo({ top: 0, behavior: 'smooth' });

    try {
      await api.completeAssessment(aid);
      // Brief animation pause for smooth clinical transition
      setTimeout(() => {
        navigate('assessment-detail', aid);
      }, 1000);
    } catch (err) {
      console.error('Failed to complete assessment:', err);
      // Fallback navigate to result
      navigate('assessment-detail', aid);
    }
  };

  return (
    <div className="max-w-4xl mx-auto px-4 sm:px-6 py-8 space-y-8 animate-fade-in">
      {/* Top Header & Stepper */}
      <div className="space-y-4">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
          <div>
            <div className="flex items-center gap-2 text-xs font-semibold text-signal uppercase tracking-wider">
              <Stethoscope className="w-4 h-4" />
              <span>Intelligent Clinical Symptom Analyzer</span>
            </div>
            <h1 className="text-2xl sm:text-3xl font-extrabold text-mist tracking-tight mt-1">
              Comprehensive Health Evaluation
            </h1>
          </div>

          <div className="flex items-center gap-2">
            <span className="text-xs text-mist-muted font-mono">
              Step {currentStep === 'DESCRIBE' ? '1 of 4' : currentStep === 'UNDERSTAND' ? '2 of 4' : currentStep === 'CLARIFY' ? '3 of 4' : '4 of 4'}
            </span>
          </div>
        </div>

        {/* Stepper Progress Bar */}
        <div className="grid grid-cols-4 gap-2">
          {[
            { id: 'DESCRIBE', label: '1. Describe' },
            { id: 'UNDERSTAND', label: '2. Understand' },
            { id: 'CLARIFY', label: '3. Clarify' },
            { id: 'ANALYZING', label: '4. Assess' }
          ].map((s, idx) => {
            const stepOrder = ['DESCRIBE', 'UNDERSTAND', 'CLARIFY', 'ANALYZING'];
            const currentIdx = stepOrder.indexOf(currentStep);
            const isCompleted = stepOrder.indexOf(s.id) < currentIdx;
            const isCurrent = s.id === currentStep;

            return (
              <div key={s.id} className="space-y-1.5">
                <div
                  className={`h-1.5 rounded-full transition-all duration-300 ${
                    isCompleted
                      ? 'bg-mint'
                      : isCurrent
                      ? 'bg-signal'
                      : 'bg-carbon-border'
                  }`}
                />
                <span className={`text-[11px] block font-medium ${isCurrent ? 'text-signal font-semibold' : 'text-mist-muted'}`}>
                  {s.label}
                </span>
              </div>
            );
          })}
        </div>
      </div>

      {/* Emergency Alert Banner if triggered */}
      {emergencyDetected && (
        <div className="p-5 rounded-2xl glass-panel-alert border border-alert space-y-3">
          <div className="flex items-center gap-2 text-alert font-bold text-base">
            <AlertTriangle className="w-5 h-5 shrink-0" />
            <span>URGENT CLINICAL ALERT: Immediate Medical Attention Advised</span>
          </div>
          <p className="text-xs text-mist leading-relaxed">
            {emergencyMessage || 'Your reported constellation of symptoms corresponds to critical red flag criteria. Please discontinue online self-assessment and seek professional emergency care.'}
          </p>
          <div className="pt-2 flex flex-wrap items-center gap-3">
            <a
              href="tel:112"
              className="inline-flex items-center gap-2 px-4 py-2.5 rounded-xl bg-alert text-white font-bold text-xs shadow-lg hover:opacity-90 transition-opacity"
            >
              <PhoneCall className="w-4 h-4" />
              Call Emergency Dispatch (112 / 911)
            </a>
            <button
              type="button"
              onClick={() => handleCompleteAssessment()}
              className="text-xs text-mist-muted hover:text-mist underline font-medium"
            >
              View emergency clinical rationale →
            </button>
          </div>
        </div>
      )}

      {/* STEP 1: DESCRIBE */}
      {currentStep === 'DESCRIBE' && (
        <div className="space-y-8 animate-fade-in">
          {/* Natural Language Free-Text Input */}
          <div className="p-5 sm:p-6 rounded-2xl glass-panel">
            <NaturalLanguageInput
              freeText={freeText}
              onChangeFreeText={setFreeText}
              onAnalyze={handleAnalyzeNLP}
              isAnalyzing={isAnalyzingNLP}
              parseResult={nlpResult}
            />
          </div>

          {/* Symptom Tag Selector */}
          <div className="p-5 sm:p-6 rounded-2xl glass-panel">
            <SymptomTagSelector
              symptoms={symptoms}
              selectedSymptomIds={selectedSymptomIds}
              onToggleSymptom={handleToggleSymptom}
            />
          </div>

          {/* Anatomical Region Selector */}
          <div className="p-5 sm:p-6 rounded-2xl glass-panel">
            <AnatomicalRegionSelector
              locations={locations}
              selectedLocationIds={selectedLocationIds}
              onToggleLocation={handleToggleLocation}
            />
          </div>

          {/* Structured Properties Card */}
          <SymptomPropertiesCard
            duration={duration}
            severity={severity}
            character={character}
            onChangeDuration={setDuration}
            onChangeSeverity={setSeverity}
            onChangeCharacter={setCharacter}
          />

          {/* Next Button */}
          <div className="flex items-center justify-between pt-4">
            <button
              type="button"
              onClick={() => navigate('dashboard')}
              className="px-4 py-2.5 rounded-xl text-xs font-semibold text-mist-muted hover:text-mist hover:bg-carbon border border-carbon-border transition-colors flex items-center gap-2"
            >
              <ArrowLeft className="w-4 h-4" />
              <span>Cancel</span>
            </button>

            <button
              type="button"
              onClick={handleProceedToUnderstand}
              className="px-6 py-3 rounded-xl text-sm font-bold bg-signal text-void hover:opacity-90 transition-all flex items-center gap-2 shadow-lg"
            >
              <span>Review Identified Findings</span>
              <ArrowRight className="w-4 h-4" />
            </button>
          </div>
        </div>
      )}

      {/* STEP 2: UNDERSTAND (Findings Review) */}
      {currentStep === 'UNDERSTAND' && (
        <div className="space-y-6 animate-fade-in">
          <div className="p-6 rounded-2xl glass-panel space-y-6">
            <div>
              <div className="text-xs font-semibold text-signal uppercase tracking-wider flex items-center gap-2">
                <CheckCircle2 className="w-4 h-4" />
                Step 2: Review Identified Clinical Findings
              </div>
              <h2 className="text-xl font-bold text-mist mt-1">
                Please confirm the details Healix extracted from your description
              </h2>
              <p className="text-xs text-mist-muted mt-1 leading-relaxed">
                Before our rule engine runs, ensure that your symptoms, body regions, and timeframes are accurately recorded.
              </p>
            </div>

            {/* Structured Findings Table */}
            <div className="space-y-4">
              {/* Primary Complaint */}
              <div className="p-4 rounded-xl surface-card space-y-1">
                <span className="text-[10px] uppercase font-bold text-mist-muted tracking-wider">Primary Description</span>
                <p className="text-sm font-medium text-mist italic">"{freeText}"</p>
              </div>

              {/* Symptoms Identified */}
              <div className="p-4 rounded-xl surface-card space-y-2">
                <span className="text-[10px] uppercase font-bold text-mist-muted tracking-wider">Identified Symptoms</span>
                <div className="flex flex-wrap gap-2">
                  {selectedSymptomIds.map(id => {
                    const sym = symptoms.find(s => s.id === id);
                    return (
                      <span key={id} className="text-xs font-semibold px-3 py-1 rounded-lg bg-signal/15 border border-signal/30 text-signal">
                        {sym?.name || id}
                      </span>
                    );
                  })}
                  {selectedSymptomIds.length === 0 && (
                    <span className="text-xs text-mist-muted">No explicit symptom tags selected</span>
                  )}
                </div>
              </div>

              {/* Anatomical Locations */}
              <div className="p-4 rounded-xl surface-card space-y-2">
                <span className="text-[10px] uppercase font-bold text-mist-muted tracking-wider">Target Body Locations</span>
                <div className="flex flex-wrap gap-2">
                  {selectedLocationIds.map(id => {
                    const loc = locations.find(l => l.id === id);
                    return (
                      <span key={id} className="text-xs font-medium px-3 py-1 rounded-lg surface-card text-mist">
                        <MapPin className="w-3 h-3 inline mr-1 text-signal" />
                        {loc?.name || id}
                      </span>
                    );
                  })}
                  {selectedLocationIds.length === 0 && (
                    <span className="text-xs text-mist-muted">Generalized / Not localized</span>
                  )}
                </div>
              </div>

              {/* Properties Grid */}
              <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
                <div className="p-3 rounded-xl surface-card">
                  <span className="text-[10px] text-mist-muted block">Duration</span>
                  <span className="text-xs font-bold text-mist">{duration}</span>
                </div>
                <div className="p-3 rounded-xl surface-card">
                  <span className="text-[10px] text-mist-muted block">Severity</span>
                  <span className="text-xs font-bold text-mist">{severity}</span>
                </div>
                <div className="p-3 rounded-xl surface-card">
                  <span className="text-[10px] text-mist-muted block">Character / Quality</span>
                  <span className="text-xs font-bold text-mist">{character}</span>
                </div>
              </div>

              {/* Negated Facts */}
              {nlpResult?.negated_facts && nlpResult.negated_facts.length > 0 && (
                <div className="p-3 rounded-xl bg-mint/10 border border-mint/30 space-y-1">
                  <span className="text-[10px] font-bold text-mint uppercase tracking-wider">Explicitly Ruled Out By You</span>
                  <p className="text-xs text-mint">
                    {nlpResult.negated_facts.map(f => f.replace('symptom.', '').replace('_', ' ')).join(', ')}
                  </p>
                </div>
              )}
            </div>

            {/* Stepper Navigation */}
            <div className="flex items-center justify-between pt-4 border-t border-carbon-border">
              <button
                type="button"
                onClick={() => setCurrentStep('DESCRIBE')}
                className="px-4 py-2.5 rounded-xl text-xs font-semibold text-mist-muted hover:text-mist hover:bg-carbon border border-carbon-border transition-colors flex items-center gap-2"
              >
                <ArrowLeft className="w-4 h-4" />
                <span>Modify Details</span>
              </button>

              <button
                type="button"
                onClick={handleStartClarifyingQuestions}
                className="px-6 py-3 rounded-xl text-sm font-bold bg-signal text-void hover:opacity-90 transition-all flex items-center gap-2 shadow-lg"
              >
                <span>Proceed to Clarifying Questions</span>
                <ArrowRight className="w-4 h-4" />
              </button>
            </div>
          </div>
        </div>
      )}

      {/* STEP 3: CLARIFY (Adaptive Follow-Up Questions) */}
      {currentStep === 'CLARIFY' && (
        <div className="animate-fade-in space-y-6">
          {currentQuestion ? (
            <AdaptiveQuestionView
              question={currentQuestion}
              questionNumber={questionCount}
              totalAnswered={answeredCount}
              onSubmitAnswer={handleSubmitAnswer}
              isSubmitting={isSubmittingAnswer}
              onFinishEarly={() => handleCompleteAssessment()}
            />
          ) : (
            <div className="p-8 rounded-2xl glass-panel text-center space-y-4">
              <div className="w-8 h-8 border-2 border-signal border-t-transparent rounded-full animate-spin mx-auto" />
              <p className="text-sm font-semibold text-mist">Selecting the most relevant question...</p>
            </div>
          )}
        </div>
      )}

      {/* STEP 4: ANALYZING (Clinical Engine Reasoning) */}
      {currentStep === 'ANALYZING' && (
        <div className="p-12 rounded-2xl glass-panel text-center space-y-6 animate-fade-in">
          <div className="w-12 h-12 border-3 border-signal border-t-transparent rounded-full animate-spin mx-auto" />
          <div className="space-y-2">
            <h2 className="text-xl font-bold text-mist">Synthesizing Clinical Assessment</h2>
            <p className="text-xs text-mist-muted max-w-md mx-auto leading-relaxed">
              Evaluating production rules, ruling out acute vascular and neurological red flags, and generating structured clinical guidance...
            </p>
          </div>
          <div className="inline-flex items-center gap-2 px-3 py-1.5 rounded-full bg-signal/10 border border-signal/20 text-signal text-xs font-mono">
            <Activity className="w-3.5 h-3.5 animate-pulse" />
            <span>Deterministic Rule Engine Running</span>
          </div>
        </div>
      )}
    </div>
  );
};
