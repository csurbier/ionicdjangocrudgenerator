__all__ = ['ENTITY','API_SERVICE']

ENTITY="""
{% load crudcustomtags %}
{% for model in models %}

export class {{model}} {
    {% entity_filter app model %}
   
    constructor() {

    }

       
    initWithJSON(json) : {{model}}{
      for (var key in json) {
          this[key] = json[key];
      }
      return this;
    }
}
{% endfor %}
"""

API_SERVICE = """import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders, HttpParams, HttpErrorResponse } from '@angular/common/http';
import { Observable,BehaviorSubject } from 'rxjs';
import { from, of, forkJoin } from 'rxjs';
import { catchError, retry, map } from 'rxjs/operators';
import { AlertController, LoadingController } from '@ionic/angular';
import * as Constant from '../config/constant';
import { Platform } from '@ionic/angular';
import { Plugins } from '@capacitor/core';
const { Network } = Plugins;
const { Storage } = Plugins;
export enum ConnectionStatus {
    Online,
    Offline
  }

@Injectable({
    providedIn: 'root'
})
export class ApiserviceService {

    public status: BehaviorSubject<ConnectionStatus> = new BehaviorSubject(ConnectionStatus.Offline);
    public tokenSet: BehaviorSubject<Boolean> = new BehaviorSubject<Boolean>(false);

    public tokenSSO: String = "";
    networkConnected: boolean = true;
    virtualHostName: string = ''
    oAuth2ClientId: string = '';
    oAuth2ClientSecret: string = '';
    oAuth2Username: string = '';
    oAuth2Password: string = '';
    appName: string = '';
    apiPrefix = "/api"
    loader: any;
    expireDate: any;
    isOnline = false;
    // Standard url from the iDevotion Django API Fwk
    urlPwdOublie: string = '';
    checkUrl: string = '';
    cordovaiOS = false;
    isShowingLoader = false;
    getFcmUrl: string = '';
    getOauthUrl: string = '';
    getAPnsUrl: string = '';
    sendMessageUrl: string = '';
    {% for model in models %}
    get{{ model }}Url : string='';
    {% endfor %}
    initProvider(url, app_name, clientId, clientSecret, user, password, apiPrefix) {
        this.virtualHostName = url;
        this.oAuth2ClientId = clientId;
        this.oAuth2ClientSecret = clientSecret;
        this.oAuth2Username = user;
        this.oAuth2Password = password;
        this.appName = app_name;
        this.apiPrefix = apiPrefix;
        console.log("init provider appName " + this.appName);
        this.initUrls()
    }

    private initUrls() {
    //Default urls 
     this.checkUrl = this.virtualHostName + this.apiPrefix + "/checkAPI/"
     this.getFcmUrl = this.virtualHostName + "/devices/"
        this.getOauthUrl = this.virtualHostName + '/o/token/';
        this.getAPnsUrl = this.virtualHostName + "/device/apns/"
        this.sendMessageUrl = this.virtualHostName + this.apiPrefix + "/sendMessageEmail"
        {% for model in models %}
            this.get{{ model }}Url = this.virtualHostName + this.apiPrefix + "/{{ model|lower }}/"
        {% endfor %}
    }

    constructor(public http: HttpClient,
        public loadingController: LoadingController,
        public alertCtrl: AlertController,
        public platform : Platform){
            
        this.initializeNetworkEvents();

        this.initProvider(Constant.domainConfig.virtual_host, Constant.domainConfig.client,
            Constant.oAuthConfig.client_id, Constant.oAuthConfig.client_secret,
            Constant.oAuthConfig.username, Constant.oAuthConfig.password, "api")
        this.http = http
    }

    public async initializeNetworkEvents() {
        console.log("======== Initialise Network Events ======")
        if (this.platform.is("cordova")){
            let status = await Network.getStatus();
            if (status["connected"]==false){
                this.networkConnected=false
                this.updateNetworkStatus(ConnectionStatus.Offline);
            }
            else{
                this.networkConnected=true;
                this.updateNetworkStatus(ConnectionStatus.Online);
            }
            let handler = Network.addListener('networkStatusChange', (status) => {
                console.log("Network status changed", status);
                if (status["connected"]==false){
                    this.networkConnected=false
                    this.updateNetworkStatus(ConnectionStatus.Offline);
                }
                else{
                    this.networkConnected=true;
                    this.updateNetworkStatus(ConnectionStatus.Online);
                }
              });

            
            
            
        }
        else{
            if (navigator.onLine){
                this.updateNetworkStatus(ConnectionStatus.Online);
            }
            else{
                this.updateNetworkStatus(ConnectionStatus.Offline);
            }
        }
      }

      private async updateNetworkStatus(status: ConnectionStatus) {
        this.status.next(status);
        this.networkConnected = status == ConnectionStatus.Offline ? false : true;
        console.log("networkConnected "+this.networkConnected)
      }
     
      public onNetworkChange(): Observable<ConnectionStatus> {
        return this.status.asObservable();
      }
     
      public getCurrentNetworkStatus(): ConnectionStatus {
        return this.status.getValue();
      }

     
      // Local Data 
      private setLocalData(key, jsonData) {
        return new Promise(async resolve => {
        
        if (this.platform.is("cordova")){
            await Storage.set({key:`${Constant.domainConfig.client}-${key}`,value:JSON.stringify(jsonData)})
            resolve(true)
        }
        else{
            //Cache HTML5
            localStorage.setItem(`${Constant.domainConfig.client}-${key}`, JSON.stringify(jsonData));
            resolve(true)
        }
    });
      }
     
      public removeLocalData(key){
        return new Promise(async resolve => {
            let ret = await Storage.remove({key:`${Constant.domainConfig.client}_${key}`}) 
            
        });
      }
      // Get cached API result
      public getLocalData(key) {
        return new Promise(async resolve => {
            let ret = await Storage.get({key:`${Constant.domainConfig.client}_${key}`}) 
            if (ret.value){
                resolve( JSON.parse(ret.value))
            }
            else{
                resolve(null)
            }
        });
    }
    
    
     {% for model in models %}
        create{{model}}(modelToCreate) {
        // model JSON
        const options = {
            headers: new HttpHeaders({
                'Authorization': 'Bearer ' + this.tokenSSO,
                'Content-Type': 'application/json'
            })
        };

        let params = JSON.stringify(modelToCreate)
        console.log("URL "+this.get{{ model }}Url)
        return this.http.post(this.get{{ model }}Url, modelToCreate, options).pipe(retry(1))
    }
    
    find{{model}}WithQuery(query) {
        let url = this.get{{ model }}Url + query;
        return this.find{{model}}(url)
    }


    find{{model}}(url) {
        const options = {
            headers: new HttpHeaders({
                'Authorization': 'Bearer ' + this.tokenSSO,
                'Content-Type': 'application/json'
            })
        };
       
        return Observable.create(observer => {
            // At this point make a request to your backend to make a real check!
            console.log("call url " + url);
            this.http.get(url, options)
                .pipe(retry(1))
                .subscribe(res => {
                    observer.next(res);
                    observer.complete();
                }, error => {
                    observer.next();
                    observer.complete();
                    console.log(error);// Error getting the data
                });
        });
        }
        
    
    get{{model}}Details(id){
        const options = {
            headers: new HttpHeaders({
                'Authorization': 'Bearer ' + this.tokenSSO,
                'Content-Type': 'application/json'
            })
        };
        return Observable.create(observer => {
            // At this point make a request to your backend to make a real check!
            this.http.get(this.get{{model}}Url + id + "/", options)
                .pipe(retry(1))
                .subscribe(res => {
                    this.networkConnected = true
                    observer.next(res);
                    observer.complete();
                }, error => {
                    observer.next(false);
                    observer.complete();
                    console.log(error);// Error getting the data
                });
        });
    }
    update{{model}}(id, putParams) {
        const options = {
            headers: new HttpHeaders({
                'Authorization': 'Bearer ' + this.tokenSSO,
                'Content-Type': 'application/json'
            })
        };
        return Observable.create(observer => {
            // At this point make a request to your backend to make a real check!
            this.http.patch(this.get{{model}}Url + id + "/", putParams, options)
                .pipe(retry(1))
                .subscribe(res => {
                    this.networkConnected = true
                    observer.next(true);
                    observer.complete();
                }, error => {
                    observer.next(false);
                    observer.complete();
                    console.log(error);// Error getting the data
                });
        });
    }

    delete{{model}}(id) {
        const options = {
            headers: new HttpHeaders({
                'Authorization': 'Bearer ' + this.tokenSSO,
                'Content-Type': 'application/json'
            })
        };
        return  this.http.delete(this.get{{model}}Url + id + "/", options).pipe(retry(1))
                 
        
    }    
    {% endfor %}
    
       //Override 
    async showNoNetwork() {
        let alert = await this.alertCtrl.create({
            header: 'Désolé',
            message: 'Pas de réseau détecté. Merci de vérifier votre connexion 3G/4G ou Wifi',
            buttons: ['OK']
        });
        return await alert.present();

    }

    /**
    * Show a loader inside your ionic application
    *
    */
    async showLoading() {
        if (this.loader) {
            this.loader.dismiss();
            this.loader = null;
            // return
        }
        this.loader = await this.loadingController.create({
            message: 'Merci de patienter',
            duration: 5000
        });
        return await this.loader.present();
    }

    /**
    * Show a loader with a specific message inside your ionic application
    *
    */
    public async showLoadingMessage(message) {
        this.loader = await this.loadingController.create({
            message: message,
        });
        this.loader.present();
    }

    /**
    * Stop the loader inside your ionic application
    *
    */

    async stopLoading() {
        this.loader.dismiss();
        this.loader = null;
    }


    /**
    * Show error message  
    *
    * @param text - The message to show
    * 
    */
    async showError(text) {
        let alert = await this.alertCtrl.create({
            header: 'Erreur',
            message: text,
            buttons: ['OK']
        });
        return await alert.present();
    }

    /**
    * Show a message  
    *
    * @param title - The title of the message to show
    * @param message - The text of the message to show
    * 
    */
    async showMessage(title, message) {
        let alert = await this.alertCtrl.create({
            header: title,
            message: message,
            buttons: ['OK']
        });
        return await alert.present();
    }

    getExpireDate() {
        return Observable.create(async observer => {
          let date = await Storage.get({key:this.appName  + '_expireAccessToken'}) 
            if (date) {
              this.expireDate = JSON.parse(date.value);
              console.log("on met en mémoire dateExpire " + date);
              observer.next(this.expireDate);
              observer.complete();
            }
            else {
              observer.next();
              observer.complete();
            }
          })
             
      }
      

    checkOauthToken() {
        console.log("on check OAUTH TOKEN");
        return new Promise(async resolve => {
          let result = await Storage.get({key:this.appName  + '_accessToken'}) 
            console.log("OK CHECK TOKEN " + result.value);
            if (result) {
              this.tokenSSO = JSON.parse(result.value);
              // Set expire date
              let expireFS = this.getExpireDate().subscribe((date) => {
                // check date expire
                expireFS.unsubscribe()
                let now = Date.now() / 1000;
                console.log("on compare " + this.expireDate + " avec " + now);
                if (Number(this.expireDate) < now) {
                  console.log("date expirée, on va chercher nouveau token")
                  resolve()
                }
                else {
                    this.tokenSet.next(true)
                  resolve(JSON.parse(result.value))
                }
              })
            }
            else {
              resolve()
            }
          
        });
      
    }

    checkAPI() {
        return Observable.create(observer => {
            // At this point make a request to your backend to make a real check!
            this.http.get(this.checkUrl)
                .pipe(
                    retry(1)
                )
                .subscribe(res => {
                    this.networkConnected = true
                    observer.next(true);
                    observer.complete();
                }, error => {
                    observer.next(false);
                    observer.complete();
                });
        });
    }

    getOAuthToken() {
        let url = this.getOauthUrl
        console.log("pas de token appel WS url avec nouveau headers " + url);
        let body = 'client_id=' + this.oAuth2ClientId + '&client_secret=' + this.oAuth2ClientSecret + '&username=' + this.oAuth2Username + '&password=' + this.oAuth2Password + '&grant_type=password';
        //console.log("body "+body);
        const httpOptions = {
            headers: new HttpHeaders({
                'content-type': "application/x-www-form-urlencoded",
            })
        };
        return new Promise(resolve => {
            this.http.post(url, body, httpOptions)
                .pipe(
                    retry(1)
                )
                .subscribe(async res => {
                    let token = res["access_token"];
                    this.tokenSSO = token
                    console.log("ok TOKEN " + token);
                    let expireIn = res["expires_in"]; // Secondes
                    this.expireDate = (Date.now() / 1000) + expireIn;
                    // Save expireDate
                    Storage.set({key:this.appName + '_expireAccessToken',value:JSON.stringify(this.expireDate)});
                    await Storage.set({key:this.appName + '_accessToken', value:JSON.stringify(this.tokenSSO)}) 
                    this.tokenSet.next(true)
                    resolve(token)
                    
                }, error => {
                    
                    console.log("ERREUR APPEL TOKEN ");// Error getting the data
                    console.log(error)
                    resolve()
                });
        });
    }

    sendMessageEmail(email, subject, message) {
        let urlParams = "?email=" + email + "&subject=" + subject + "&message=" + message;
        let url = this.sendMessageUrl + encodeURI(urlParams);
        const httpOptions = {
            headers: new HttpHeaders({
                'Authorization': 'oAuth: ' + this.tokenSSO,
                'Content-Type': 'application/json'
            })
        };
        return new Promise(resolve => {
            this.http.get(url, httpOptions)
                .pipe(retry(1))
                .subscribe(res => {
                    resolve(res)
                }, error => {
                    console.log(error);// Error getting the data
                    resolve()
                });
        });
    }


    sendFcmToken(tokenId, deviceName, typeDevice) {
        const options = {
            headers: new HttpHeaders({
                'Authorization': 'Bearer ' + this.tokenSSO,
                'Content-Type': 'application/json'
            })
        };
        let postParams = {
            "name": deviceName,
            "registration_id": tokenId,
            "active": true,
            "type": typeDevice
        };
        
        return Observable.create(observer => {
            // At this point make a request to your backend to make a real check!
            this.http.post(this.getFcmUrl, postParams, options)
                .pipe(retry(1))

                .subscribe(res => {
                    this.networkConnected = true
                    observer.next(true);
                    observer.complete();
                }, error => {
                    observer.next(false);
                    observer.complete();
                    console.log(error);// Error getting the data
                });
        });
    }
}
"""
