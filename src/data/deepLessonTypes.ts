export type DeepFormula = {
  id: string;
  title: string;
  latex: string;
  variables: { symbol: string; meaning: string; unit: string }[];
  assumptions: string[];
  domain: string;
  interpretation: string;
};

export type DeepSection = {
  moduleId: string;
  title: string;
  lead: string;
  paragraphs: string[];
  keyPoints: string[];
  miniExample?: {
    title: string;
    setup: string;
    walkthrough: string[];
    takeaway: string;
  };
};

export type DeepWorkedExample = {
  id: string;
  moduleIds: string[];
  title: string;
  given: string[];
  find: string;
  plan: string;
  steps: { label: string; latex?: string; result: string }[];
  interpret: string;
  sanityCheck: string;
};

export type DeepAssessment = {
  id: string;
  objectiveIds: string[];
  skill: "calculation" | "application" | "diagnosis" | "transfer";
  prompt: string;
  options: { id: "A" | "B" | "C" | "D"; text: string; feedback: string }[];
  correctOptionId: "A" | "B" | "C" | "D";
  solution: string[];
};

export type DeepLesson = {
  readingId: number;
  title: string;
  sections: DeepSection[];
  formulas: DeepFormula[];
  workedExamples: DeepWorkedExample[];
  misconceptions: { claim: string; correction: string; diagnostic?: string }[];
  assessments: DeepAssessment[];
};
