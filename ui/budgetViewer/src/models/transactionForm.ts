import { FormlyFieldConfig } from "@ngx-formly/core";
import * as moment from "moment";


export interface SearchTransactionsForm {
  bankAction: string;
  startDate: string;
  endDate: string;
  transDescript: string;
  numberOfResults : number;
}
export class Transaction {

  id : number
  bankAction: string;
  transactonDescript : string;
  amount : number;
  createdAt: string


  public constructor(...args: any[]) {
    if (args.length === 1) {
      // logic for your called constructor goes here..
      this.intialize(args[0])
    }



  }
  intialize(data: Transaction) {
    this.bankAction = data.bankAction 
    this.transactonDescript = data.transactonDescript
    this.amount = data.amount
    this.id = data.id
    
    this.createdAt = moment(data.createdAt).format('YYYY-MM-DD')
  }


}

export class TransactionForm {
  bankAction: string;
  startDate: string;
  endDate: string;
  transDescript: string;
  numberOfResults : number;
  public constructor(...args: any[]) {
    if (args.length === 1) {
      // logic for your called constructor goes here..
      this.intialize(args[0])
    }



  }
  intialize(data: SearchTransactionsForm) {
    this.bankAction = data.bankAction
    this.numberOfResults = data.numberOfResults
    if(data.transDescript != undefined|| data.transDescript != null )
    {
      this.transDescript= data.transDescript
    }else{
      this.transDescript= ''
    }

    if(data.numberOfResults != undefined|| data.numberOfResults != null )
    {
      this.numberOfResults= data.numberOfResults
    }else{
      this.numberOfResults= 10
    }
    

    this.startDate = moment(data.startDate).format('YYYY-MM-DD')
    this.endDate = moment(data.endDate).format('YYYY-MM-DD')
  }


}