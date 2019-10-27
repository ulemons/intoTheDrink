import { Component, OnInit, Injectable } from '@angular/core';
import SampleJson from '../assets/metrics.json';
import { HttpClient } from '@angular/common/http';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})


@Injectable
export class AppComponent implements OnInit {
  title = 'intoTheDrink';
  torbidity = 243;
  colour = 111;
  temp = 111;
  ph = 111;
  co2 = 111;


  
 data: string[];

    constructor(private configService: ConfigService) {}

    ngOnInit() {
        this.data = this.configService.getConfiguration().matrixFile;
    }

}
