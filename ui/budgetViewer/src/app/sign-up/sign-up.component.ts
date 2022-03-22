import { Component, OnInit } from '@angular/core';
 import { FormBuilder,FormGroup,Validators } from '@angular/forms';
import { FormlyField, FormlyFieldConfig } from '@ngx-formly/core';
import { UserAccount, UserForm } from '../../models/user';
import { AuthService } from '../shared/services/auth.service';
 
@Component({
  selector: 'app-sign-up',
  templateUrl: './sign-up.component.html',
  styleUrls: ['./sign-up.component.css']
})
export class SignUpComponent  {
  form = new FormGroup({});
  userModel  = new UserAccount();
  fields: FormlyFieldConfig[] = [
    
    {
      key: 'firstName',
      type: 'input',
      templateOptions: {
        label: 'First Name',
        placeholder: 'name',
        required: true,
      },
    },
    {
      key: 'lastName',
      type: 'input',
      templateOptions: {
        label: 'Last Name',
        placeholder: 'name',
        required: true,
      },
    },
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
    {
      key: 'passwordConfirm',
      type: 'input',
      templateOptions: {
        type: 'password',
        label: 'Confirm Password',
        placeholder: 'Please re-enter your password',
        required: true,
      },
    },
    
  ];
  constructor(private authService: AuthService) {}

  submit(userModel: UserAccount){
    this.authService.singUpAccount(userModel)
    console.log(userModel)
  }



}