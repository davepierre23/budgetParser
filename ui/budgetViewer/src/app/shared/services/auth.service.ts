import { Injectable } from '@angular/core';
import { UserForm, Users} from "../../../models/user"
import { Router } from "@angular/router";
//https://fireship.io/lessons/angularfire-google-oauth/
import { Observable, of ,from} from 'rxjs';
import { switchMap} from 'rxjs/operators';
import { HttpClient } from '@angular/common/http';

@Injectable({
  providedIn: 'root'
})
export class AuthService {
  private serverUrl = 'http://localhost:8000/users';
  dbName:string = "users"
  userLogInData :any  = null;
  user$?: Observable<Users | null | undefined> = of(null);
  constructor(
    private httpClient: HttpClient,
    public router: Router,
  ) {}

  updateUserData(user:any, userForm:UserForm) {

    const data:Users = {
      uid: user.uid,
      email: user.email,
      displayName: `${userForm.firstName} ${userForm.lastName}` ,
    }
    //return userRef.set(data, { merge: true })
  }
  // used to Sign in account and provide authenication whenever
  singUpAccount(userForm: any){
    
    return this.httpClient.post(this.serverUrl, userForm).subscribe(
      (data) => {
        console.log(data)
      
      }
  );
 
  }
  login(userForm: any){
    console.log("service")
    return this.httpClient.post(this.serverUrl, userForm).subscribe(
      (data) => {
        console.log(data)
      
      }
  );
 
  }

//check to see if there a Users Observable set already
get authenciatedUser(): Observable<Users | null | undefined>{
  if(this.user$){
    return this.user$
  }else{
    return of(null)
  }
}

}