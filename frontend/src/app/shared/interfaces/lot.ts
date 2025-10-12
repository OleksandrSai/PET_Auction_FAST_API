import {BidInterface} from './bid';

export interface LotInterface {
  id: number;
  title: string;
  start_price: number;
  state: string;
  image_url: string;
  start_time: string;
  end_time: string;
  bids: BidInterface[];
  max_bid: number;
  created_at: string;
  expand?: boolean;
}

export enum LotState {
  RUNNING = "RUNNING",
  ENDED = "ENDED",
  ARCHIVED = "ARCHIVED",
  SCHEDULED = "SCHEDULED",
  CANCELLED = "CANCELLED",
}
