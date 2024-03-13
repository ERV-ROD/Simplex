import { Component, OnInit} from '@angular/core';
import { ApiService } from 'src/app/services/api.service';

@Component({
  selector: 'data-collector',
  templateUrl: './data-collector.component.html',
  styleUrls: ['./data-collector.component.scss']
})
export class DataCollectorComponent implements OnInit{
  functionVariables:number[] = [];
  equationEqual:number[] = [];
  equationVariables:number[][] = [];
  selectedSymbols:number[] = [];
  variables: number = 0;
  constraints: number = 0;
  type: string = 'Max';

  constructor(public service:ApiService){}

  ngOnInit(): void {
    for(let i = 0; i < this.constraints; i++){
      this.selectedSymbols[i] = 1;
    }
  }

  saveFunctionVariables() {
    const functionVariables: number[] = []
    for (let i = 0; i < this.variables; i++) {
      const inputElement = document.getElementById(`x${i + 1}`) as HTMLInputElement;
      if (inputElement) {
        functionVariables.push(parseFloat(inputElement.value));
      }
    }
    this.functionVariables = functionVariables;
  }

  saveEquationEqual() {
    const equationSolutions: number[] = []
    for (let i = 0; i < this.constraints; i++) {
      const inputElement = document.getElementById(`z${i + 1}`) as HTMLInputElement;
      if (inputElement) {
        equationSolutions.push(parseFloat(inputElement.value));
      }
    }
    this.equationEqual = equationSolutions
  }

  saveEquationVariables() {
    const equationVariables: number[][] = [];
    for (let j = 0; j < this.constraints; j++) {
      const equation: number[] = [];
      for (let i = 0; i < this.variables; i++) {
        const inputElement = document.getElementById(`y${i + 1 + j * 10}`) as HTMLInputElement;
        if (inputElement) {
          equation.push(parseFloat(inputElement.value));
        }
      }
      equationVariables.push(equation);
    }
    this.equationVariables = equationVariables;
  }

  onSymbolChange(event: any){
    const id = parseInt(event.target.id);
    if(event.target){
      const selectedValue = event.target.value;
      this.selectedSymbols[id] = parseInt(selectedValue);
    }
  }

  updateSymbolsArray(numbers2add:number){
    for(let i = 0; i < numbers2add; i++){
      this.selectedSymbols.push(1);
    }
  }


  saveAllData(){
    this.saveFunctionVariables();
    console.log("func: ", this.functionVariables)
    this.saveEquationVariables();
    console.log("equa: ", this.equationVariables)
    this.saveEquationEqual();
    console.log("equal ", this.equationEqual)
    console.log("symbol ", this.selectedSymbols)

    const json2send = {
      functionVariables: this.functionVariables,
      equationEqual: this.equationEqual,
      equationVariables: this.equationVariables,
      selectedSymbols: this.selectedSymbols,
      variables: this.variables,
      constraints: this.constraints,
      type: this.type
    }
    console.log("llego")
    console.log("json ", json2send)
    this.service.sendData(json2send);
  }
  


  /**
   * The function updates the value of the "constraints" variable based on the selected value from an
   * event target.
   * 
   * @param event The event parameter is an object that represents the event that triggered the
   * function. It contains information about the event, such as the target element that triggered the
   * event.
   */
  onConstraintsChange(event: any){
    if(event.target){
      const selectedValue = event.target.value;
      this.constraints = parseInt(selectedValue, 10)
    }
    const len = this.constraints - this.selectedSymbols.length;
    if(len > 0){
      this.updateSymbolsArray(len);
    }
  }

  /**
   * The function updates the value of a variable based on the selected value from an event.
   * 
   * @param event The event parameter is of type "any", which means it can be any type of object. It is
   * used to capture the event that triggered the variable change.
   */
  onVariableChange(event: any){
    if(event.target){
      const selectedValue =  event.target.value;
      this.variables = parseInt(selectedValue, 10);
    }
  }

  /**
   * The function updates the value of the "type" variable based on the selected value from an event.
   * 
   * @param event The event parameter is an object that represents the event that triggered the
   * onTypeChange function. It contains information about the event, such as the target element that
   * triggered the event.
   */
  onTypeChange(event: any){
    if(event.target){
      const selectedValue = event.target.value;
      this.type = selectedValue;
    }
  }


  /**
   * The function "numberOfVariables" creates an array with a specified number of elements.
   * 
   * @param variables The parameter "variables" is a number that represents the number of variables you
   * want to create.
   * 
   * @return An array with the specified number of elements.
   */
  numberOfVariables(variables: number){
    return new Array(variables);
  }

  /**
   * The function returns an array with a specified number of elements.
   * 
   * @param constraints The parameter "constraints" is a number that represents the number of
   * constraints you want to create.
   * 
   * @return An array with the length equal to the value of the "constraints" parameter.
   */
  numberOfConstraints(constraints: number){
    return new Array(constraints);
  }
}
