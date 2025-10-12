import {Component, computed, Input} from '@angular/core';
import {LotState} from '../../../shared/interfaces/lot';
import {Timer} from './timer/timer';
import {BidInterface} from '../../../shared/interfaces/bid';
import {DatePipe} from '@angular/common';

@Component({
  selector: 'app-lot-status',
  imports: [Timer, DatePipe],
  templateUrl: './lot-status.html',
  styleUrl: './lot-status.scss'
})

export class LotStatus {
 @Input() state?: string;
 @Input() startTime?: string;
 @Input() endTime?: string;
 @Input() numberOfBets: number = 0;
 @Input() bids?: BidInterface[];

LotStateLabels: Record<LotState, string> = {
  [LotState.RUNNING]: "⏳ Running",
  [LotState.ENDED]: "✅ Ended",
  [LotState.ARCHIVED]: "📦 Archived",
  [LotState.SCHEDULED]: "🗓️ Scheduled",
  [LotState.CANCELLED]: "❌ Cancelled",
};

highestBid = computed<BidInterface | null>(() => {
  if (!this.bids || this.bids.length === 0) return null;
  return this.bids.reduce((max, bid) =>
    bid.amount > max.amount ? bid : max
  );
});

currentStateLabel = computed(() => {
  if (!this.state) return '—';
  console.log(this.state)
  return this.LotStateLabels[this.state as LotState] || 'Unknown';
});



}
