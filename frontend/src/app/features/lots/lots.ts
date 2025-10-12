import {Component, OnInit} from '@angular/core';
import {NzTableModule} from 'ng-zorro-antd/table';
import {NzInputModule} from 'ng-zorro-antd/input';
import {NzSelectModule} from 'ng-zorro-antd/select';
import {FormsModule} from '@angular/forms';
import {NzPaginationModule} from 'ng-zorro-antd/pagination';
import { NzButtonModule } from 'ng-zorro-antd/button';
import {NgTemplateOutlet} from '@angular/common';
import {LotService} from '../../core/services/lot-service';
import {LotInterface} from '../../shared/interfaces/lot';
import { NzIconModule } from 'ng-zorro-antd/icon';
import {LotStatus} from './lot-status/lot-status';


@Component({
  selector: 'app-lots',
  imports: [NzTableModule, NzButtonModule, NzInputModule, NzSelectModule, FormsModule, NzPaginationModule,
    NgTemplateOutlet, NzIconModule, LotStatus],
  templateUrl: './lots.html',
  standalone: true,
  styleUrl: './lots.scss'
})
export class Lots implements OnInit{
  protected pageSizes: number[] = [10, 25, 50];
  protected _pageSize: string = '10';
  protected totalItems: number = 20;
  protected pageIndex: number = 1 ;
  private searchText: string = "";
  protected expandSet = new Set<number>();
  public pageDataArr: LotInterface[] = [];
  public meterIdReadindNow: null | number = null;
  constructor(protected lotService: LotService) {
  }
  ngOnInit(): void {
    this.loadData()
  }


  get pageSize(): number {
    return Number(this._pageSize);
  }
  onExpandChange(id: number, checked: boolean): void {
    if (checked) {
      this.expandSet.add(id);
    } else {
      this.expandSet.delete(id);
    }
  }
  onPageIndexChange(newPageIndex: number): void {
    this.pageIndex = newPageIndex;
    this.loadData();
  }

  openWindowCreateLot(){

  }

  loadData(): void{
   this.lotService.getAllLots(this.pageIndex, this.pageSize).subscribe((res: LotInterface[])=>{
        this.pageDataArr = res;
        console.log(this.pageDataArr)
   })
  }

  onPageSizeChange(event: Event): void {
    this.loadData();
  }

  search(value: string): void {
    this.pageIndex = 1;
    this.searchText = value;
    this.loadData();
  }


}
