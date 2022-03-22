import { HttpClient, HttpEventType } from '@angular/common/http';
import { Component, Input } from '@angular/core';
import { finalize, Subscription } from 'rxjs';
import {UploadService} from '../shared/services/upload.service'
import { FormGroup } from '@angular/forms';
import { FormlyFormOptions, FormlyFieldConfig } from '@ngx-formly/core';


@Component({
  selector: 'app-upload',
  templateUrl: './upload.component.html',
  styleUrls: ['./upload.component.css']
})
export class UploadComponent {
  fileToUpload: File | null = null;
     // Variable to store shortLink from api response
    sucessOrFail: string = "";
    loading: boolean = false; // Flag variable

    form = new FormGroup({});
    model = {};
    options: FormlyFormOptions = {};
    fields: FormlyFieldConfig[] = [
      {
        key: 'file',
        type: 'file',
      },
    ];
    constructor(private uploadService: UploadService) {}

    handleFileInput(event: Event) {
      // this.fileToUpload = files.item(0);
      this.fileToUpload = (event.target as HTMLInputElement).files[0];
      console.log( this.fileToUpload )

  }
  createResponseMessage(result: String, fileName:String){
    if(result == "sucess"){
      this.sucessOrFail =  fileName +" has successfully been delivered"
    }else{
      this.sucessOrFail =  fileName +" has  failed"
    }
  }

  // OnClick of button Upload
  onUpload() {
    this.loading = !this.loading;
    console.log("")
    this.uploadService.upload(this.fileToUpload!).subscribe(
        (data) => {
          this.createResponseMessage(data.result,this.fileToUpload!.name)
          
         
         this.loading = false; // Flag variable 
            
        }
    );
}


}