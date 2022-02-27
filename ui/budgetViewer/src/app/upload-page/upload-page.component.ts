import { Component } from '@angular/core';
import {UploadService} from '../shared/services/upload.service'

@Component({
  selector: 'app-upload-page',
  templateUrl: './upload-page.component.html',
  styleUrls: ['./upload-page.component.css']
})
export class UploadPageComponent {


  constructor(private uploadService: UploadService) {}



}
