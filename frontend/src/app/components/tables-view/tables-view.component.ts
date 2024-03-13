import { Component, OnDestroy, OnInit} from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { ApiService } from 'src/app/services/api.service';
import { Subscription } from 'rxjs';
import { saveAs } from 'file-saver';

@Component({
  selector: 'app-tables-view',
  templateUrl: './tables-view.component.html',
  styleUrls: ['./tables-view.component.scss']
})
export class TablesViewComponent implements OnInit, OnDestroy {
  responseData: any;
  tables: any;
  RCPair: any;
  variables: any;
  constraints: any;
  addedVariables: any;
  type: any;

  //=============== Columnas y Filas =====================//
  columns: any;
  rows: any;

  private responseDataSubscription: Subscription = new Subscription();

  constructor(private apiService: ApiService, private http: HttpClient) {
    this.columns = [];
    this.rows = [];
  }

  ngOnInit() {
    this.responseDataSubscription = this.apiService.getResponseDataObservable().subscribe(
      (response) => {

        this.responseData = response;
        console.log('Respuesta del servidor en responseData:', this.responseData);

        this.tables = this.responseData.tables
        this.RCPair = this.responseData.RCPair;
        this.variables = this.responseData.variables;
        this.constraints = this.responseData.constraints;
        this.addedVariables = this.responseData.addedVariables;
        this.type = this.responseData.type;

        this.genereteRC(this.addedVariables[0],this.addedVariables[1]);

        console.log(this.tables);
        console.log(this.tables[this.tables.length-1][1]);
        console.log(this.tables[this.tables.length-1][2]);
        console.log(this.tables[this.tables.length-1][1][this.columns.length]);
        console.log(this.tables[this.tables.length-1][2][this.columns.length]);
        console.log(this.rows);
      },
      (error) => {
        console.error('Error al obtener la respuesta del servidor:', error);
      }
    );
  }

  ngOnDestroy() {
    this.responseDataSubscription.unsubscribe();
  }

  genereteRC(artificial: any, slack: any) {
    const columnSet: string[] = [];
    const rowSet: string[] = [];

    for(let i = 1; i <= this.variables; i++){
      columnSet.push('X' + i);
    }

    for (let i = 1; i <= slack; i++) {
      columnSet.push('S' + i);
      rowSet.push('S' + i);
    }

    for (let i = 1; i <= artificial; i++) {
      columnSet.push('R' + i);
      rowSet.push('R' + i);
    }
    this.columns = columnSet;
    this.rows = [rowSet];
    this.generateNextRows();
  }  

  generateNextRows() {
    for (let i = 0; i < this.RCPair.length; i++) {
      let newRow: any = this.rows[i].slice();
      newRow[this.RCPair[i][0]-1] = this.columns[this.RCPair[i][1]];
      this.rows.push(newRow);
    }
  }

  getCSV() {
    this.http.get('http://localhost:5000/download/csv', {
      responseType: 'blob',
    }).subscribe((response: any) => {
      const blob = new Blob([response], { type: 'text/csv' });
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = 'tabla.csv';
      document.body.appendChild(a);
      a.click();
      window.URL.revokeObjectURL(url);
    });
  }
}
