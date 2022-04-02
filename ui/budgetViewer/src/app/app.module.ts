import { NgModule, CUSTOM_ELEMENTS_SCHEMA } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { ReactiveFormsModule } from '@angular/forms';
import { FormlyModule } from '@ngx-formly/core';
import { FormlyMaterialModule } from '@ngx-formly/material';
import {BrowserAnimationsModule} from '@angular/platform-browser/animations'
import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { UploadComponent } from './upload/upload.component';
import { UploadService } from './shared/services/upload.service';
import { AuthService } from './shared/services/auth.service';
import { MaterialModule } from './shared/modules/material/material.module';
import { UploadPageComponent } from './upload-page/upload-page.component';
import { HttpClientModule, HTTP_INTERCEPTORS } from '@angular/common/http';
import { HeaderBarComponent } from './header-bar/header-bar.component';
import { NavigationBarComponent } from './navigation-bar/navigation-bar.component';
import { SignInComponent } from './sign-in/sign-in.component';
import { SignUpComponent } from './sign-up/sign-up.component';
import { ErrorPageComponent } from './error-page/error-page.component';
import { SearchTransactionsFormComponent } from './search-transactions-form/search-transactions-form.component';
import { SearchTransactionsPageComponent } from './search-transactions-page/search-transactions-page.component';
 
import { FormlyMatDatepickerModule } from '@ngx-formly/material/datepicker';
import { MatNativeDateModule } from '@angular/material/core';
import { TransactionSearchTableComponent } from './transaction-search-table/transaction-search-table.component';
@NgModule({
  declarations: [
    AppComponent,
    UploadComponent,
    UploadPageComponent,
    HeaderBarComponent,
    NavigationBarComponent,
    SignInComponent,
    SignUpComponent,
    ErrorPageComponent,
    SearchTransactionsFormComponent,
    SearchTransactionsPageComponent,
    TransactionSearchTableComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    MaterialModule,
    BrowserAnimationsModule,
    HttpClientModule,  
    ReactiveFormsModule,
    FormlyModule.forRoot({
      validationMessages: [
        { name: 'required', message: 'This field is required' },
      ],
    }),
    MatNativeDateModule,
    FormlyMatDatepickerModule,
    FormlyMaterialModule
  ],
  schemas: [
    CUSTOM_ELEMENTS_SCHEMA
  ],
  providers: [AuthService,UploadService],
  bootstrap: [AppComponent]
})
export class AppModule { }
