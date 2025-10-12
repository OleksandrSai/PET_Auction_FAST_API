import {Component, Input, OnDestroy, OnInit, signal} from '@angular/core';

@Component({
  selector: 'app-timer',
  imports: [],
  templateUrl: './timer.html',
  styleUrl: './timer.scss'
})
export class Timer implements OnInit, OnDestroy {

  @Input() startTime?: string;
  @Input() endTime?: string;

  remainingTime = signal(0);

  private intervalId?: number;

  ngOnInit() {
    if (!this.endTime) return;

    const end = new Date(this.endTime).getTime();

    this.updateRemainingTime(end);

    this.intervalId = window.setInterval(() => this.updateRemainingTime(end), 1000);
  }
  private updateRemainingTime(end: number) {
    const now = Date.now();
    const diff = Math.floor((end - now) / 1000);
    this.remainingTime.set(diff);
  }

  public formatTime(seconds: number): string {
    const h = Math.floor(seconds / 3600);
    const m = Math.floor((seconds % 3600) / 60);
    const s = seconds % 60;
    return `${h.toString().padStart(2,'0')}:${m.toString().padStart(2,'0')}:${s.toString().padStart(2,'0')}`;
  }
  ngOnDestroy() {
    if (this.intervalId) clearInterval(this.intervalId);
  }

}
