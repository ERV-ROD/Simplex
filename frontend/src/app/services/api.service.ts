import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Subject } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class ApiService {

  constructor(private http:HttpClient) { }

  private url: string = "http://localhost:5000/post/data"
  private responseDataSubject = new Subject<any>();

  sendData(json:any){
  
    this.http.post(this.url, json)
    .subscribe(
      (response) => {
        console.log('Respuesta del servidor:', response);
        this.responseDataSubject.next(response);
      },
      (error) => {
        console.error('Error al enviar el JSON:', error);
      }
    );
  }
  getResponseDataObservable() {
    return this.responseDataSubject.asObservable();
  }
}
