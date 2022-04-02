import { AfterViewInit, Component, ViewChild, OnInit, Input } from '@angular/core';
import { MatPaginator } from '@angular/material/paginator';
import { MatSort } from '@angular/material/sort';
import { MatTableDataSource } from '@angular/material/table';

 import { Transaction } from '../../models/transactionForm';
import { TransactionsService } from '../shared/services/transactions.service';
import { of, Observable, Subject, Subscription } from 'rxjs';
import { catchError, map, switchMap, tap } from 'rxjs/operators';

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
  @ViewChild(MatSort) sort!: MatSort;

  // @Input()
  transactions$: Observable<(Transaction | undefined)[]> = of([]);
  transactionSubscription!: Subscription;

  constructor(private  dataService:  TransactionsService) {}



  ngAfterViewInit() {
    this.transactions$=this.dataService.getAll()

    if (this.transactions$) {
      this.transactionSubscription = this.transactions$.subscribe((data) => {
        console.log('is loading ', this.isLoading);
        console.log('data going into bookcodes', data);
        if (data) {
          this.dataSource = new MatTableDataSource(data);
          this.dataSource.paginator = this.paginator;
          setTimeout(() => (this.dataSource.paginator = this.paginator));
        }
      });
    } else {
      this.transactions$ = of([]);
    }
  }

  ngOnDestroy() {
    this.transactionSubscription.unsubscribe();
  }
}


