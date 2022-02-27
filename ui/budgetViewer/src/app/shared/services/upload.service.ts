import { Injectable } from '@angular/core';
import { HttpClient, HttpRequest, HttpEvent } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class UploadService {

  private serverUrl = 'http://localhost:8000/saveFile';

  constructor(private httpClient: HttpClient) { }

  // upload(file: File): Observable<HttpEvent<any>> {
  //   const formData: FormData = new FormData();

  //   formData.append('file', file);

  //   const request = new HttpRequest('POST', `${this.serverUrl}/upload`, formData, {
  //     reportProgress: true,

  //   });

  //   return this.httpClient.request(request);
  // }

  // Returns an observable
  upload(file: File):Observable<any> {
  
    // Create form data
    const formData = new FormData(); 
      
    // Store form name as "file" with file data
    formData.append("uploadedFile", file, file.name);
      
    // Make http post request over api
    // with formData as req
    return this.httpClient.post(this.serverUrl, formData)
}
  getFiles(): Observable<any> {
    return this.httpClient.get(`${this.serverUrl}/files`);
  }
}
