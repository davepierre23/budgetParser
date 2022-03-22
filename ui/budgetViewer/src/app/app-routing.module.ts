import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';


//Importing all the compenented that I would like to navigate through pages
import { SignInComponent } from './sign-in/sign-in.component';
import { SignUpComponent } from './sign-up/sign-up.component';
import { AuthGuard } from "./shared/guard/auth.guard";
import { LoginGuard } from "./shared/guard/login.guard";
import { ErrorPageComponent } from './error-page/error-page.component';
import { UploadPageComponent } from './upload-page/upload-page.component';
import { SearchTransactionsPageComponent } from './search-transactions-page/search-transactions-page.component';

const routes: Routes = [
  { path: '', redirectTo: 'sign-in', pathMatch: 'full'},
 // { path: 'sign-in', component: SignInComponent, canActivate: [LoginGuard]},
 { path: 'sign-in', component: SignInComponent},
 { path: 'sign-up', component: SignUpComponent},
 { path: 'search', component: SearchTransactionsPageComponent},
 { path: 'upload', component: UploadPageComponent},
  { path: '**', component: ErrorPageComponent  }   // default routing will be sign in componente
]

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
