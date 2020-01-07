import { Injectable } from '@angular/core';
import { Http } from '@angular/http';
import { Configuration } from './configuration';
import { map } from 'rxjs/operators';

import { HttpClient } from '@angular/common/http'; 
import { Observable } from 'rxjs';

@Injectable()
export class ConfigService {
  constructor(private http: HttpClient) {
    this.getJSON().subscribe(data => {
        console.log(data);
    });
}

public getJSON(): Observable<any> {
    return this.http.get("./assets/matrix.json");
}

  /*private config: Configuration;

  constructor(private http: Http) {
  }

  load(url: string) {
    return new Promise((resolve) => {
      this.http.get(url).pipe(map(data => {}))
        .subscribe(config => {
          console.log(config);
          //this.config = config;
          resolve();
        });
    });
  }

  getConfiguration(): Configuration {
    return this.config;
  }
*/
}
