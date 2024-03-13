import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { DataCollectorComponent } from './components/data-collector/data-collector.component';

const routes: Routes = [
  {path: 'simplex', component:  DataCollectorComponent}
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
