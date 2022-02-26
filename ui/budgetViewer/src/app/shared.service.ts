import { Injectable } from '@angular/core';
import { HttpClient} from '@angular/common/http'
import {Observable} from 'rxjs'
@Injectable({
  providedIn: 'root'
})
export class SharedService {

  constructor(private http:HttpClient) { }
  API_URL  = 'http://localhost:8000/SaveFile'

  getTranscations(): Observable<any[]>{
    return this.http.get<any[]>(this.API_URL)
  }
}
