export interface IData {
  id: number
  total: string
  date: string
  file: string
  author: number
  agent_id: number
  comment_id: number
  username: string
}

export interface IForm {
  comment: string;
  total: number;
  file: File | null;
  agent_id: number; 
}
