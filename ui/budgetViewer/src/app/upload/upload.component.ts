import { HttpClient, HttpEventType } from '@angular/common/http';
import { Component, Input } from '@angular/core';
import { finalize, Subscription } from 'rxjs';
import {UploadService} from '../shared/services/upload.service'

@Component({
  selector: 'app-upload',
  templateUrl: './upload.component.html',
  styleUrls: ['./upload.component.css']
})
export class UploadComponent {
  fileToUpload: File | null = null;
     // Variable to store shortLink from api response
    shortLink: string = "";
    loading: boolean = false; // Flag variable
    constructor(private uploadService: UploadService) {}

    handleFileInput(event: Event) {
      // this.fileToUpload = files.item(0);
      this.fileToUpload = (event.target as HTMLInputElement).files[0];
      console.log( this.fileToUpload )

  }


  // OnClick of button Upload
  onUpload() {
    this.loading = !this.loading;
    this.uploadService.upload(this.fileToUpload!).subscribe(
        (event: any) => {
            if (typeof (event) === 'object') {

                // Short link via api response
                this.shortLink = event.link;

                this.loading = false; // Flag variable 
            }
        }
    );
}
}