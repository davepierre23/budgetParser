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

    formFields(){
      return <FormlyFieldConfig[]>[
        {
          key: 'firstName',
          type: 'input',
          templateOptions: {
            label: 'firstName',
            placeholder: 'firstName',
            required: true,
          },
          validation:{
            messages:{
              required: 'You need to provide a first name!'
            }
          }
        },
        {
          key: 'lastName',
          type: 'input',
          templateOptions: {
            label: 'lastName',
            placeholder: 'lastName',
            required: true,
          },
          validation:{
            messages:{
              required: 'You need to provide a last name!'
            }
          }
        },
        {
          key: 'email',
          type: 'input',
          templateOptions: {
            label: 'email',
            placeholder: 'Email',
            required: true,
          },
          validation:{
            messages:{
              required: 'You need to provide a email!'
            }
          }
        },
      ]
    }

  }