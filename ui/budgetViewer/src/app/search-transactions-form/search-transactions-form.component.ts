import { Component, OnInit } from '@angular/core';
import { FormBuilder,FormGroup,Validators } from '@angular/forms';
import { FormlyField, FormlyFieldConfig, FormlyFormOptions } from '@ngx-formly/core';
import { UserAccount, UserForm } from '../../models/user';
import { TransactionsService } from '../shared/services/transactions.service';
 
@Component({
  selector: 'search-transactions-form',
  templateUrl: './search-transactions-form.component.html',
  styleUrls: ['./search-transactions-form.component.css']
})
export class SearchTransactionsFormComponent   {

  form = new FormGroup({});
  model  = new UserAccount();
  options: FormlyFormOptions = {};
  fields: FormlyFieldConfig[] = [
    
    {
      key: 'bankAction',
      type: 'select',
      templateOptions: {
        label: 'Select a Bank Action',
        required: true,
        options: [
          { value: 'W', label: 'Withdraw'  },
          { value: 'D', label: 'Deposit'  },
        ],
      },
    },

    {
      key: 'startDate',
      type: 'datepicker',
      templateOptions: {
        label: 'Start Date Ex: 3/22/2022',
        required: true,
      },
    },
    {
      key: 'endDate',
      type: 'datepicker',
      templateOptions: {
        label: 'End Date Ex: 3/22/2022',
        required: true,
      },
    },
    
  ];
  constructor(private transactionService:TransactionsService ) {}

  submit(model: any){
    this.transactionService.search(model)
    console.log(model)
  }



}