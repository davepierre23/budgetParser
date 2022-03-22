import { Injectable } from '@angular/core';
import { UserForm, Users} from "../../../models/user"
import { Router } from "@angular/router";
//https://fireship.io/lessons/angularfire-google-oauth/
import { Observable, of ,from} from 'rxjs';
import { catchError, switchMap} from 'rxjs/operators';
import { HttpClient, HttpParams } from '@angular/common/http';

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

  getAll(model: any){
    
    return this.httpClient.get(this.serverUrl).subscribe(
      (data) => {
        console.log(data)
      
      }
  );
 
  }
  search(model: any){
    var params : HttpParams = new HttpParams()

    let key: keyof any;
    for (key in model) {  // let k: "a" | "b" | "c"
      const value = model[key];  // Type is string | number
      params = params.set(key, value)
      
    }
    


    const options =
    { params:params } ;
    const thing =this.httpClient.get(this.serverUrl+this.detail, options).subscribe(
      (data) => {
        console.log(data)
      
      }
  );
 
  
  }


}