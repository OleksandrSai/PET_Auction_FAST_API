import {Bid} from './bid';

export interface LotInterface {
  id: number;
  title: string;
  start_price: number;
  state: string;
  image_url: string;
  start_time: string;
  end_time: string;
  bids: Bid[];
  max_bid: number;
  created_at: string;
}
