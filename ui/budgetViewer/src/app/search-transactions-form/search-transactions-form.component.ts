import { Component, OnInit } from '@angular/core';
import { FormBuilder,FormGroup,Validators } from '@angular/forms';
import { FormlyField, FormlyFieldConfig, FormlyFormOptions } from '@ngx-formly/core';
import { TransactionForm, SearchTransactionsForm } from '../../models/transactionForm';
import { TransactionsService } from '../shared/services/transactions.service';
import * as moment from 'moment'; 
@Component({
  selector: 'search-transactions-form',
  templateUrl: './search-transactions-form.component.html',
  styleUrls: ['./search-transactions-form.component.css']
})
export class SearchTransactionsFormComponent   {

  form = new FormGroup({});
  model  = new TransactionForm();
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
    {
      key: 'transDescript',
      type: 'input',
      templateOptions: {
        label: 'Enter search word',
      },
    },
    {
      key: 'numberOfResults',
      type: 'select',
      templateOptions: {
        label: 'Select a number of results ',
        required: true,
        options: [
          { value: 10, label: '10'  },
          { value: 20, label: '20'  },          
          { value: 30, label: '30'  },
          { value: 40, label: '40'  },
          { value: 50, label: '50'  }

        ],
      },
    },
  ];
  constructor(private transactionService:TransactionsService ) {}

  submit(model: any){
    let search = new TransactionForm(model)
    console.log(search)
    this.transactionService.search(search)

  }



}