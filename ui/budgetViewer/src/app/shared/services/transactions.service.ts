import { Injectable } from '@angular/core';
import { UserForm, Users} from "../../../models/user"
import { Router } from "@angular/router";
//https://fireship.io/lessons/angularfire-google-oauth/
import { Observable, of ,from} from 'rxjs';
import { catchError, map, switchMap} from 'rxjs/operators';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Transaction } from 'src/models/transactionForm';

@Injectable({
  providedIn: 'root'
})
export class TransactionsService {
  private serverUrl = 'http://localhost:8000/transactions';
  private detail = '/details'
   constructor(
    private httpClient: HttpClient,
    public router: Router,
  ) {}

  getAll():Observable<Transaction[]> {
    
    return this.httpClient.get<Transaction[]>(this.serverUrl).pipe(map(result => result.map((data)=>{
      data = new Transaction(data)
      return data
    })));
 
  }
  search(model: any):Observable<Transaction[]> {
    var params : HttpParams = new HttpParams()

    let key: keyof any;
    for (key in model) {  // let k: "a" | "b" | "c"
      const value = model[key];  // Type is string | number
      params = params.set(key, value)
      
    }
    


    const options =
    { params:params } ;

    return this.httpClient.get<Transaction[]>(this.serverUrl+this.detail, options).pipe(map(result => result.map((data)=>{
      data = new Transaction(data)
      return data
    })));
  
  }


}