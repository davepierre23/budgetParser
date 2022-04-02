import { AfterViewInit, Component, ViewChild, OnInit, Input } from '@angular/core';
import { MatPaginator } from '@angular/material/paginator';
import {MatSort, Sort} from '@angular/material/sort';import { MatTableDataSource } from '@angular/material/table';

 import { Transaction } from '../../models/transactionForm';
import { TransactionsService } from '../shared/services/transactions.service';
import { of, Observable, Subject, Subscription } from 'rxjs';
import { catchError, map, switchMap, tap } from 'rxjs/operators';
import { LiveAnnouncer } from '@angular/cdk/a11y';

@Component({
  selector: 'app-transaction-search-table',
  templateUrl: './transaction-search-table.component.html',
  styleUrls: ['./transaction-search-table.component.css']
})

export class TransactionSearchTableComponent implements AfterViewInit {

  query: string = '';
  isLoading = false;
  displayedColumns: string[] = ['id', 'bankAction','transactonDescript', 'amount','createdAt'];




  dataSource!: MatTableDataSource<any>;

  @ViewChild(MatPaginator) paginator!: MatPaginator;
  @ViewChild(MatSort, { static: false }) sort!: MatSort;

  // @Input()
  transactions$: Observable<(Transaction | undefined)[]> = of([]);
  transactionSubscription!: Subscription;

  totalCost : Observable<number> = of(0)
  constructor(private _liveAnnouncer: LiveAnnouncer,private  dataService:  TransactionsService) {}



  ngAfterViewInit() {
    this.transactions$=this.dataService.getAll()
    if (this.transactions$) {
      this.transactionSubscription = this.transactions$.subscribe((data) => {
        console.log('data going into transulations', data);
        if (data) {
          this.dataSource = new MatTableDataSource(data);
          this.dataSource.sort = this.sort;
          this.dataSource.paginator = this.paginator;
          this.totalCost = this.getTotalCost(data)
          this.totalCost.subscribe(data=>{
            console.log('Total amount', this.totalCost);          console.log('Total amount', data);
          })
        }
      });
    } else {
      this.transactions$ = of([]);
    }
  }
  getTotalCost(transactions: Transaction[]): Observable<number>  {

    return of(transactions!.map(t => t!.amount).reduce((acc, value) => acc + value, 0));
  }
 /** Announce the change in sort state for assistive technology. */
 announceSortChange(sortState: Sort) {
  // This example uses English messages. If your application supports
  // multiple language, you would internationalize these strings.
  // Furthermore, you can customize the message to add additional
  // details about the values being sorted.
  if (sortState.direction) {
    this._liveAnnouncer.announce(`Sorted ${sortState.direction}ending`);
  } else {
    this._liveAnnouncer.announce('Sorting cleared');
  }
}

  ngOnDestroy() {
    this.transactionSubscription.unsubscribe();
  }
}


