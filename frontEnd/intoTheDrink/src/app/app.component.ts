import { Component, OnInit, Injectable } from '@angular/core';
import SampleJson from '../assets/metrics.json';
import { HttpClient } from '@angular/common/http';
import { ConfigService } from './servizio';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent implements OnInit {
  title = 'intoTheDrink';
  torbidity = 0;
  colour = 0;
  temp = 0;
  ph = 0;
  co2 = 0;
  alchol = 0;
  outputClass = "EMPTY";
 data: {};

    constructor( private http: HttpClient) {}

    ngOnInit() {
        this.http.get("./assets/metrics.json").subscribe(data => {
          console.log(data);
          this.torbidity = data["torb"];
          this.colour = data["camera"];
          this.co2 = data["co2"];
          this.ph = data["ph"];
          this.temp = data["temp"];
          this.alchol = data["alchol"];
          
          let rgb = this.hexToRgb(this.colour)
          for (var key in rgb) {
            if (rgb.hasOwnProperty(key)) {
                console.log(key, rgb[key]);
            }
          }
          let level = parseInt(data["level"]);
          if(level < 1200) { this.outputClass = "EMPTY"}
          else if(rgb['r'] < 30){ this.outputClass = "RED"}
          else {this.outputClass = "WHITE"}
          console.log("RGB: "+this.outputClass);
      });

        /*this.data = this.configService.getJSON().subscribe(data => {
          console.log(data);
      });*/
    }

    hexToRgb(hex) {
      var result = /^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i.exec(hex);
      return result ? {
        r: parseInt(result[1], 16),
        g: parseInt(result[2], 16),
        b: parseInt(result[3], 16)
      } : {r:125,g:180,b:150};
    }

}
