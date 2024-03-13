import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { HttpClientModule, HTTP_INTERCEPTORS } from '@angular/common/http';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { DataCollectorComponent } from './components/data-collector/data-collector.component';
import { TablesViewComponent } from './components/tables-view/tables-view.component';

@NgModule({
  declarations: [
    AppComponent,
    DataCollectorComponent,
    TablesViewComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    HttpClientModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
