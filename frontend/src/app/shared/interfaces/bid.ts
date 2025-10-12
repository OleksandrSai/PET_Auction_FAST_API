import {UserBids} from './user';

export interface Bid {
  amount: number;
  state: number;
  lot_id: number;
  user_id: number;
  created_at: string;
  user: UserBids;
}
