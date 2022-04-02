import { FormlyFieldConfig } from "@ngx-formly/core";

export interface Users {
    uid: string;
    email: string;
    displayName: string;
  }
   export interface UserForm {
    emailAddress: string;
    password: string;
    firstName: string;
    lastName: string;
  }

  export class UserAccount{
    emailAddress: string;
    password: string;
    firstName: string;
    lastName: string;

  }