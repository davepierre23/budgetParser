import { Component, OnInit } from '@angular/core';
import { FormBuilder, Validators } from '@angular/forms';
import { UserAccount, Users } from '../../models/user';
import { AuthService } from '../shared/services/auth.service';
import { Observable } from 'rxjs';
import { Router } from '@angular/router';
import {FormGroup} from '@angular/forms';
import {FormlyFormOptions,FormlyFieldConfig} from '@ngx-formly/core';

@Component({
  selector: 'app-sign-in',
  templateUrl: './sign-in.component.html',
  styleUrls: ['./sign-in.component.css']
})
export class SignInComponent  {

  form = new FormGroup({});
  userModel  = new UserAccount();

  options: FormlyFormOptions = {};
  constructor(private authService: AuthService) {}
  fields: FormlyFieldConfig[] = [
 
    {
      key: 'email',
      type: 'input',
      templateOptions: {
        label: 'Email',
        placeholder: 'myemail@adress.com',
        required: true,
      },
      validators: {
        email: {
          expression: (c:any) => /^[\w-\.]+@([\w-]+\.)+[\w-]{2,4}$/.test(c.value),
          message: (error:any, field: FormlyFieldConfig) => `"${field.formControl.value}" is not a valid email Address`,
        },
      },
    },
    {
      key: 'password',
      type: 'input',
      templateOptions: {
        type: 'password',
        label: 'Password',
        placeholder: 'Must be at least 3 characters',
        required: true,
        minLength: 3,
      },
    },
  ];

  submit(userModel: UserAccount){
    this.authService.login(userModel)
    console.log(userModel)
  }

  
}