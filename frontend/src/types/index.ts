export type Role = "ADMIN" | "COMMERCIAL" | "MANAGER";
export type Status =
  | "NEW"
  | "QUALIFIED"
  | "CONTACTED"
  | "FOLLOW_UP"
  | "NEGOTIATION"
  | "CONVERTED"
  | "LOST"
  | "LATER";
export type Priority = "LOW" | "MEDIUM" | "HIGH" | "VERY_HIGH";

export interface User {
  id: number;
  name: string;
  email: string;
  role: Role;
  is_active: boolean;
}

export interface Company {
  id: number;
  name: string;
  industry?: string | null;
  website?: string | null;
  email?: string | null;
  phone?: string | null;
  address?: string | null;
  city?: string | null;
  country?: string | null;
  employee_count?: number | null;
  description?: string | null;
  source?: string | null;
}

export interface Prospect {
  id: number;
  company_id: number;
  assigned_to?: number | null;
  score: number;
  priority: Priority;
  status: Status;
  notes?: string | null;
  estimated_value?: number | null;
  created_at: string;
  company?: Company | null;
  assigned_user?: User | null;
}

export interface Contact {
  id: number;
  prospect_id: number;
  first_name: string;
  last_name: string;
  job_title?: string | null;
  email?: string | null;
  phone?: string | null;
  linkedin_url?: string | null;
}

export interface Activity {
  id: number;
  prospect_id: number;
  user_id: number;
  type: string;
  subject: string;
  description?: string | null;
  created_at: string;
  result?: string | null;
}

export interface FollowUp {
  id: number;
  prospect_id: number;
  assigned_to: number;
  due_date: string;
  reminder_date?: string | null;
  status: string;
  notes?: string | null;
}

export interface Conversion {
  id: number;
  prospect_id: number;
  converted_by: number;
  converted_at: string;
  department: string;
  value?: number | null;
  notes?: string | null;
}

export interface Qualification {
  score: number;
  level: string;
  priority: Priority;
  summary: string;
  criteria: { label: string; points: number; explanation: string }[];
}

export interface AIAnalysis {
  score: number;
  reasoning: string;
  recommendation: string;
  potential_needs: string[];
  suggested_priority: string;
  next_action: string;
  outreach_message: string;
  provider: string;
}

export interface DashboardData {
  total: number;
  new: number;
  qualified: number;
  to_follow: number;
  converted: number;
  lost: number;
  conversion_rate: number;
  potential_value: number;
  by_status: Record<string, number>;
  by_priority: Record<string, number>;
  by_industry: Record<string, number>;
  evolution: { date: string; count: number }[];
  monthly_conversions: { month: string; count: number; value: number }[];
  today_follow_ups: FollowUp[];
  priority_prospects: Prospect[];
}
