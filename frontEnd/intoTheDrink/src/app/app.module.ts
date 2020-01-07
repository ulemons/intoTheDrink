import { HttpClient, HttpHandler } from '@angular/common/http';
import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { APP_INITIALIZER } from '@angular/core';

import { ConfigService } from './servizio';
import { environment } from '../environments/environment';

import { HttpClientModule } from '@angular/common/http'; 
@NgModule({
  declarations: [
    AppComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    HttpClientModule
  ],
  providers: [
    /*  ConfigService,
    /*{
      provide   : APP_INITIALIZER,
      useFactory: ConfigLoader,
      deps      : [ConfigService],
      multi     : true
    }*/
 ],
  bootstrap: [AppComponent]
})
export class AppModule { }
/*
export function ConfigLoader(configService: ConfigService) {
  return () => configService.load(environment.matrixFile);
}*/
