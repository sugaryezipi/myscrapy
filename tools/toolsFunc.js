//自己的工具
sandBox={
    envFuncs:{},
    config:{},
    flags:{},
    asyncCode:{},
    filter:{}
}
sandBox.config.proxy=true
sandBox.config.printLog=true
//过滤proxy
sandBox.filter.NoProxy=['Plugin','mimetype','mimetypeArray','pluginArray','window.RegExp','eval']
//防止重复代理
sandBox.flags.proxyFlag=Symbol('flag')
//获取原型对象的flag
sandBox.flags.protoFlag=Symbol("proto")
//存放标签
sandBox.tags=[]
//存放cookie
sandBox.cookieJar={
    length:0,
    cookie:{}
}
//插件
sandBox.pluginArray=undefined
sandBox.mimetypeArray=undefined
//异步事件
sandBox.asyncCode.eventListener= {}
sandBox.asyncCode.setTimeout= []
sandBox.asyncCode.setInterval= []
sandBox.asyncCode.Promise= []
sandBox.asyncCode.timeoutID=-1
sandBox.asyncCode.intervalID=-1

//document.all
sandBox.all = new ldObj();

!function () {
    //parse url
    sandBox.parseUrl = function parseUrl(str) {
        if (!parseUrl || !parseUrl.options) {
            parseUrl.options = {
                strictMode: false,
                key: ["href", "protocol", "host", "userInfo", "user", "password", "hostname", "port", "relative", "pathname", "directory", "file", "search", "hash"],
                q: {
                    name: "queryKey",
                    parser: /(?:^|&)([^&=]*)=?([^&]*)/g
                },
                parser: {
                    strict: /^(?:([^:\/?#]+):)?(?:\/\/((?:(([^:@]*)(?::([^:@]*))?)?@)?([^:\/?#]*)(?::(\d*))?))?((((?:[^?#\/]*\/)*)([^?#]*))(?:\?([^#]*))?(?:#(.*))?)/,
                    loose: /^(?:(?![^:@]+:[^:@\/]*@)([^:\/?#.]+):)?(?:\/\/)?((?:(([^:@]*)(?::([^:@]*))?)?@)?([^:\/?#]*)(?::(\d*))?)(((\/(?:[^?#](?![^?#\/]*\.[^?#\/.]+(?:[?#]|$)))*\/?)?([^?#\/]*))(?:\?([^#]*))?(?:#(.*))?)/
                }
            };
        }
        if (!str) {
            return '';
        }
        var o = parseUrl.options,
            m = o.parser[o.strictMode ? "strict" : "loose"].exec(str),
            urlJson = {},
            i = 14;
        while (i--) urlJson[o.key[i]] = m[i] || "";
        urlJson[o.q.name] = {};
        urlJson[o.key[12]].replace(o.q.parser, function($0, $1, $2) {
            if ($1) urlJson[o.q.name][$1] = $2;
        });
        delete  urlJson["queryKey"];
        delete  urlJson["userInfo"];
        delete  urlJson["user"];
        delete  urlJson["password"];
        delete  urlJson["relative"];
        delete  urlJson["directory"];
        delete  urlJson["file"];
        urlJson["protocol"] += ":";
        urlJson["origin"] = urlJson["protocol"] + "//" + urlJson["host"];
        urlJson["search"] = urlJson["search"] && "?" + urlJson["search"];
        urlJson["hash"] = urlJson["hash"] && "#" + urlJson["hash"];
        return urlJson;
    }
    sandBox.getTagJson = function (tagStr){
        let arrList = tagStr.match("<(.*?)>")[1].split(" ");
        let tagJson = {};
        tagJson["type"] = arrList[0];
        tagJson["prop"] = {};
        for(let i=1;i<arrList.length;i++){
            let item = arrList[i].split("=");
            let key = item[0];
            let value = item[1].replaceAll("\"","").replaceAll("'","");
            tagJson["prop"][key] = value;
        }
        return tagJson;
    }


    //mimeType数组
    sandBox.pushMimeTypeArray=function (mimetype) {
        let mimetypeArray=sandBox.mimetypeArray;
        if(mimetypeArray===undefined){
            mimetypeArray={}
            Object.setPrototypeOf(mimetypeArray,MimeTypeArray.prototype)
            mimetypeArray=sandBox.proxy(mimetypeArray,`mimetypeArray`)
            sandBox.setProtoAttribute.call(mimetypeArray,'length',0)
        }
        let flag=true
        for(let i=0;i<mimetypeArray.length;i++){
            if(mimetypeArray[i].type===mimetype.type){
                flag=false
            }
        }
        if(flag){
            mimetypeArray[mimetypeArray.length]=mimetype
            Object.defineProperty(mimetypeArray,mimetype.type,{value: mimetype, writable: false, enumerable: false, configurable: true})
            sandBox.setProtoAttribute.call(mimetypeArray,'length',mimetypeArray.length+1)
        }
        sandBox.mimetypeArray=mimetypeArray
        return mimetypeArray
    }
    //mimeType
    sandBox.createMimetype=function (mimeData,plugin) {
        let mimetype={}
        Object.setPrototypeOf(mimetype,MimeType.prototype)
        mimetype=sandBox.proxy(mimetype,`mimetype`)
        sandBox.setProtoAttribute.call(mimetype,'description',mimeData.description)
        sandBox.setProtoAttribute.call(mimetype,'enabledPlugin',plugin)
        sandBox.setProtoAttribute.call(mimetype,'suffixes',mimeData.suffixes)
        sandBox.setProtoAttribute.call(mimetype,'type',mimeData.type)
        sandBox.pushMimeTypeArray(mimetype)
        return mimetype
    }
    //插件数组
    sandBox.pushPluginArray=function (plugin) {
        let pluginArray=sandBox.pluginArray;
        if(pluginArray===undefined){
            pluginArray={}
            Object.setPrototypeOf(pluginArray,PluginArray.prototype)
            pluginArray=sandBox.proxy(pluginArray,`pluginArray`)
            sandBox.setProtoAttribute.call(pluginArray,'length',0)
        }
        pluginArray[pluginArray.length]=plugin
        Object.defineProperty(pluginArray,plugin.name,{value: plugin, writable: false, enumerable: false, configurable: true})
        sandBox.setProtoAttribute.call(pluginArray,'length',pluginArray.length+1)
        sandBox.pluginArray=pluginArray
        return pluginArray
    }
    //创建插件
    sandBox.createPlugin=function (data) {
        let plugin={}
        Object.setPrototypeOf(plugin,Plugin.prototype)
        plugin=sandBox.proxy(plugin,`Plugin`)
        sandBox.setProtoAttribute.call(plugin,'description',data.description)
        sandBox.setProtoAttribute.call(plugin,'filename',data.filename)
        sandBox.setProtoAttribute.call(plugin,'name',data.name)
        sandBox.setProtoAttribute.call(plugin,'length',data.mimetypes.length)
        for(let i=0;i<data.mimetypes.length;i++){
            let mimetype=sandBox.createMimetype(data.mimetypes[i],plugin)
            plugin[i]=mimetype
            Object.defineProperty(plugin,data.mimetypes[i].type,{value: mimetype, writable: false, enumerable: false, configurable: true})
        }
        sandBox.pushPluginArray(plugin)
        return plugin
    }

    //native保护函数
    !function () {
        const _mytoString=Function.prototype.toString
        const _symbol=Symbol()

        function _toString() {
            if(typeof this==="function" && this[_symbol]){
                return this[_symbol]
            }
            return _mytoString.call(this)
        }

        function setNative(func,key,value) {
            Object.defineProperty(func,key,{
                configurable:true,
                enumerable:false,
                writable:true,
                value:value
            })
        }

        delete Function.prototype.toString
        setNative(Function.prototype,"toString",_toString)
        setNative(Function.prototype.toString,_symbol,'function toString() { [native code] }')
            sandBox.setNative=function (func,funcName){
                setNative(func,_symbol,`function ${funcName || func.name}() { [native code] }`)
            }
    }()

    //获取tags标签
    sandBox.getCollections=function (objName){
        let collections=[]
        for(const index in sandBox.tags){
            if(sandBox.getType(sandBox.tags[index])===objName){
                collections.push(sandBox.tags[index])
            }
        }
        return collections
    }
    
    //获取原型对象属性
    sandBox.getProtoAttribute=function (key) {
        if(this[sandBox.flags.protoFlag]){
            return this[sandBox.flags.protoFlag][key]
        }
        return `getProtoAttribute->${key}未定义`
    }


    sandBox.setProtoAttribute=function (key,v) {
        if(!(sandBox.flags.protoFlag in this)){
            Object.defineProperty(this,sandBox.flags.protoFlag,{
                configurable:false,
                enumerable:false,
                writable:true,
                value:{}
            })
        }
        this[sandBox.flags.protoFlag][key]=v
        return v
    }

    //创建标签ID
    sandBox.getID=function () {
        if(!sandBox.flags.elementID){
            sandBox.flags.elementID=0
        }
        sandBox.flags.elementID+=1
        return sandBox.flags.elementID
    }

    //函数转发
    sandBox.dispatch=function (name,self,argList,defaultValue) {
        if(Object.getOwnPropertyDescriptor(self,'constructor')!==undefined){
            sandBox.throwError('TypeError','Illegal invocation')
        }
        try{
            return sandBox.envFuncs[name].apply(self,argList)
        }catch (e) {
            if(defaultValue!==undefined) {
                return defaultValue
            }
            console.log(`{tools|dispatch -> 环境缺失:${name} ->错误:${e.message}`)
        }
    }

    //自定义defineproperty
    sandBox.defineProperty=function (obj,prop,oldDescriptor) {
        let newDescriptor={}
        newDescriptor.configurable=sandBox.config.proxy|| oldDescriptor.configurable
        newDescriptor.enumerable=oldDescriptor.oldDescriptor
        if(oldDescriptor.hasOwnProperty("writable")){
            newDescriptor.writable=sandBox.config.proxy|| oldDescriptor.writable
        }
        if(oldDescriptor.hasOwnProperty("value")){
            let value=oldDescriptor.value
            if(typeof value==='function'){
                sandBox.safeFunc(value,prop)
            }
            newDescriptor.value=value
        }
        if(oldDescriptor.hasOwnProperty("get")){
            let get=oldDescriptor.get
            if(typeof get==='function'){
                sandBox.safeFunc(get,`get ${prop}`)
            }
            newDescriptor.get=get
        }
        if(oldDescriptor.hasOwnProperty("set")){
            let set=oldDescriptor.set
            if(typeof set==='function'){
                sandBox.safeFunc(set,`set ${prop}`)
            }
            newDescriptor.set=set
        }

        Object.defineProperty(obj,prop,newDescriptor)
    }

    //重命名函数
    sandBox.reName=function (func,funcName) {
        Object.defineProperty(func,"name",{
            configurable:true,
            enumerable:false,
            writable:false,
            value:funcName
        })
    }
    //原型重命名
    sandBox.reNameProto=function (obj,objName) {
        Object.defineProperty(obj.prototype,Symbol.toStringTag,{
            configurable:true,
            enumerable:false,
            writable:false,
            value:objName
        })
    }
    //保护原型
    sandBox.safeProto=function (obj,objName) {
        sandBox.reNameProto(obj,objName)
        sandBox.setNative(obj,objName)
    }
    //保护函数
    sandBox.safeFunc=function (func,funcName) {
        sandBox.reName(func,funcName)
        sandBox.setNative(func,funcName)
    }

    sandBox.hook=function (func,funcInfo,isDebug,onEnter,onLeval,isExec) {
        if(typeof func!='function'){
            return func
        }
        if(funcInfo===undefined){
            funcInfo={
                objName:"globalThis",
                funcName:func.name || ''
            }
        }
        if(isDebug===undefined){
            isDebug=false
        }
        if(!onEnter){
            onEnter=function (obj){
                console.log(`{hook|${funcInfo.objName}[${funcInfo.funcName}]函数执行前传入的参数:${JSON.stringify(obj.args)}}`)
            }
        }
        if(!onLeval){
            onLeval=function (obj) {
                console.log(`{hook|${funcInfo.objName}[${funcInfo.funcName}]函数执行后生成的结果:${obj.result?obj.result.toString():[]}}`)
            }
        }
        if(isExec===undefined){
            isExec=true
        }

        hookFunc=function hookFunc() {
            if(isDebug){
                debugger;
            }
            let obj={};
            obj.args=[]
            for(let i=0;i<arguments.length;i++){
                obj.args[i]=arguments[i]
            }
            //函数执行前
            onEnter.call(this,obj)
            let result
            if(isExec){
                //函数执行中
                result=func.apply(this,obj.args)
            }
            obj.result=result
            //函数执行后
            onLeval.call(this,obj)
            return obj.result
        };
        //保护代码
        sandBox.setNative(hookFunc,funcInfo.funcName);
        sandBox.reName(hookFunc,funcInfo.funcName);

        return hookFunc
    }

    sandBox.hookObj=function (obj,objName,propName,isDebug) {
        let oldDescriptor=Object.getOwnPropertyDescriptor(obj,propName)
        let newDescriptor={}
        if(oldDescriptor.configurable==false){
            return;
        }
        newDescriptor.configurable=true
        newDescriptor.enumerable=oldDescriptor.enumerable;
        if(oldDescriptor.hasOwnProperty("writable")){
            newDescriptor.writable=oldDescriptor.enumerable
        }
        if(oldDescriptor.hasOwnProperty("value")){
            let funcInfo={
                objName:objName,
                funcName:propName
            }
            newDescriptor.value=sandBox.hook(oldDescriptor.value,funcInfo,isDebug)
        }
        if(oldDescriptor.hasOwnProperty("get")){
            let funcInfo={
                objName:objName,
                funcName:`get ${propName}`
            }
            newDescriptor.get=sandBox.hook(oldDescriptor.get,funcInfo,isDebug)
        }
        if(oldDescriptor.hasOwnProperty("set")){
            let funcInfo={
                objName:objName,
                funcName:`set ${propName}`
            }
            newDescriptor.set=sandBox.hook(oldDescriptor.set,funcInfo,isDebug)
        }
        Object.defineProperty(obj,propName,newDescriptor)
    }

    sandBox.hookProto=function (obj,isDebug) {
        let protoObj=obj.prototype
        for(const key in Object.getOwnPropertyDescriptors(protoObj)){
            sandBox.hookObj(protoObj,obj.name,key,isDebug)
        }
        console.log(`{hookProto|${protoObj}}`)
    }

    sandBox.hookGlobal=function (isDebug){
        for(const key in Object.getOwnPropertyDescriptors(window)){
            if(typeof window[key]==='function'){
                if(typeof window[key].prototype==='object'){
                    sandBox.hookProto(window[key],isDebug)
                }
                else if (typeof window[key].prototype==='undefined'){
                    let funcInfo={
                        objName:"globalThis",
                        funcName:key
                    }
                    sandBox.hook(window[key],funcInfo,isDebug)
                }
            }
        }
        console.log("{hook|globalThis}")
    }

    sandBox.getType=function (obj) {
        return Object.prototype.toString.call(obj)
    }

    sandBox.proxy=function (obj,objName) {
        //过滤不代理的
        if(sandBox.filter.NoProxy.includes(objName)){
            return obj
        }
        if(!sandBox.config.proxy){
            return obj
        }
        if(sandBox.flags.proxyFlag in obj){
            return obj[sandBox.flags.proxyFlag]
        }
        let handler={
            get(target,p,receiver){
                let result;
                try{
                    result=Reflect.get(target,p,receiver)
                    if(sandBox.flags.proxyFlag===p || p==="eval"){
                        return result;
                    }
                    let type=sandBox.getType(result)
                    if (p.toString()==='createElement'){
                        debugger;
                    }
                    if(result instanceof Object){
                        console.log(`{obj|get:[${objName}] -> prop:[${p.toString()}] -> type:[${type}]}`)
                        result=sandBox.proxy(result,`${objName}.${p.toString()}`)
                    }else if(typeof result==='symbol'){
                        console.log(`{obj|get:[${objName}] -> prop:[${p.toString()}] -> result:[${result.toString()}]}`)
                    }else{
                        console.log(`{obj|get:[${objName}] -> prop:[${p.toString()}] -> result:[${result}]}`)

                    }
                }catch (e) {
                    console.log(`{obj|get:${objName} -> prop:${p.toString()} -> error:${e.message}}`)
                }
                return result
            },
            set(target, p, newValue, receiver){
                let result;
                try{
                    result=Reflect.set(target, p, newValue, receiver)
                    let type=sandBox.getType(newValue)
                    if(newValue instanceof Object){
                        console.log(`{obj|set:[${objName}] -> prop:[${p.toString()}] -> newValue_type:[${type}]}`)
                    }else if(typeof newValue==="symbol"){
                        console.log(`{obj|set:[${objName}] -> prop:[${p.toString()}] -> result:[${newValue.toString()}]}`)
                    }else{
                        console.log(`{obj|set:[${objName}] -> prop:[${p.toString()}] -> newValue:[${newValue}]}`)
                    }
                }catch (e) {
                    console.log(`{obj|set:${objName} -> prop:${p.toString()} -> error:${e.message}}`)
                }
                return result
            },
            // getOwnPropertyDescriptor(target, p) {
            //     let result;
            //     try{
            //         result=Reflect.getOwnPropertyDescriptor(target,p)
            //         let type=sandBox.getType(result)
            //         // if(typeof result!=="undefined"){
            //         //     result=sandBox.proxy(result,`${objName}.${p.toString()}.property`)
            //         // }
            //         console.log(`{obj|getOwnPropertyDescriptor:[${objName}] -> prop:[${p.toString()}] -> result:[${JSON.stringify(result)}]}`)
            //     }catch (e) {
            //         console.log(`{obj|getOwnPropertyDescriptor:${objName} -> prop:${p.toString()} -> error:${e.message}}`)
            //     }
            //     return result
            // },
            defineProperty(target, p, attributes) {
                let result;
                try{
                    result=Reflect.defineProperty(target,p,attributes)
                    console.log(`{obj|defineProperty:[${objName}] -> prop:[${p.toString()}] -> result:[${JSON.stringify(attributes)}]}`)
                }catch (e) {
                    console.log(`{obj|defineProperty:${objName} -> prop:${p.toString()} -> error:${e.message}}`)
                }
                return result
             },
            apply(target, thisArg, argArray) {
                let result;
                try{
                    result=Reflect.apply(target, thisArg, argArray)
                    let type=sandBox.getType(result)
                    //获取参数
                    let args = argArray.map(arg => {
                       if (typeof arg === "function") {
                            return `function ${arg.name||''}`;
                        } else if (arg instanceof Object) {
                        try {
                          return JSON.stringify(arg);
                        } catch (e) {
                          return arg.toString();
                        }
                      } else if (typeof arg === "symbol") {
                        return arg.toString();
                      } else {
                        return arg;
                      }
                    });
                    if(result instanceof Object){
                        console.log(`{func|apply:[${objName}] -> type:[${type}] ->args:[${args}]}`)
                    }else if(typeof result ==="symbol"){
                        console.log(`{func|apply:[${objName}] -> result:[${result.toString()}]} ->args:[${args}]`)
                    }else{
                        console.log(`{func|apply::[${objName}] -> result:[${result}] ->args:[${args}]}`)
                    }

                }catch (e) {
                    console.log(`{func|apply:${objName} -> error:${e.message}}`)
                }
                return result
            },
            construct(target, argArray, newTarget) {
                let result;
                try{
                    result=Reflect.construct(target, argArray, newTarget)
                    let type=sandBox.getType(result)
                    console.log(`{obj|construct:[${objName}] -> type:[${type}]}`)
                }catch (e) {
                    console.log(`{obj|construct:${objName} -> error:${e.message}}`)
                }
                return result
            },
            has(target, p) {
                let result;
                try{
                    result=Reflect.has(target,p)
                    if(sandBox.flags.proxyFlag !==p){
                        console.log(`{obj|has:[${objName}] -> prop:[${p.toString()}] -> has:[${result}]}`)
                    }
                }catch (e) {
                    console.log(`{obj|has:${objName} -> error:${e.message}}`)
                }
                return result
            },
            deleteProperty(target, p) {
                let result;
                try{
                    result=Reflect.deleteProperty(target,p)
                    console.log(`{obj|deleteProperty:[${objName}] -> prop:[${p.toString()}] -> result:[${result}]}`)
                }catch (e) {
                    console.log(`{obj|deleteProperty:${objName} -> error:${e.message}}`)
                }
                return result
            },
            getPrototypeOf(target) {
                let result;
                try{
                    result=Reflect.getPrototypeOf(target)
                    console.log(`{obj|getPrototypeOf:[${objName}]}`)
                }catch (e) {
                    console.log(`{obj|getPrototypeOf:${objName} -> error:${e.message}}`)
                }
                return result
            },
            setPrototypeOf(target, v) {
                let result;
                try{
                    result=Reflect.setPrototypeOf(target,v)
                    console.log(`{obj|setPrototypeOf:[${objName}]}`)
                }catch (e) {
                    console.log(`{obj|setPrototypeOf:${objName} -> error:${e.message}}`)
                }
                return result
            },
            preventExtensions(target){
                let result = Reflect.preventExtensions(target);
                try{
                    console.log(`{obj|preventExtensions:[${objName}]}`);
                }catch (e) {
                    console.log(`{obj|preventExtensions:${objName} -> error:${e.message}}`)
                }
                return result;
            },
            isExtensible(target){
                let result = Reflect.isExtensible(target);
                try{
                    console.log(`{obj|isExtensible:[${objName}]}`);
                }catch (e) {
                    console.log(`{obj|isExtensible:${objName} -> error:${e.message}}`)
                }
                return result;
            },
            ownKeys: function (target){
                let result = Reflect.ownKeys(target);
                try{
                    console.log(`{obj|ownKeys:[${objName}]}`);
                }catch (e) {
                    console.log(`{obj|ownKeys:${objName} -> error:${e.message}}`)
                }
                return result
            },
        }
        let resultProxy=new Proxy(obj,handler)
        Object.defineProperty(obj,sandBox.flags.proxyFlag,{
            configurable:false,
            enumerable:false,
            writable:false,
            value:resultProxy
        })
        return resultProxy
    }

    //报错函数
    sandBox.throwError=function (name,message) {
        let myError=new Error()
        myError.name=name
        myError.message=message
        myError.stack= `${name}: ${message}\n    at <anonymous>:1:4`
        throw myError
    }

    //实现base64编码解码
    sandBox.base64={}
    sandBox.base64.btoa=function btoa(str) {
        function base64Encode(str) {
          let base64EncodeChars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/";
          let out = "", i = 0, len = str.length;
          let c1, c2, c3;

          while (i < len) {
            c1 = str.charCodeAt(i++) & 0xff;
            if (i == len) {
              out += base64EncodeChars.charAt(c1 >> 2);
              out += base64EncodeChars.charAt((c1 & 0x3) << 4);
              out += "==";
              break;
            }
            c2 = str.charCodeAt(i++);
            if (i == len) {
              out += base64EncodeChars.charAt(c1 >> 2);
              out += base64EncodeChars.charAt(((c1 & 0x3)<< 4) | ((c2 & 0xF0) >> 4));
              out += base64EncodeChars.charAt((c2 & 0xF) << 2);
              out += "=";
              break;
            }
            c3 = str.charCodeAt(i++);
            out += base64EncodeChars.charAt(c1 >> 2);
            out += base64EncodeChars.charAt(((c1 & 0x3)<< 4) | ((c2 & 0xF0) >> 4));
            out += base64EncodeChars.charAt(((c2 & 0xF) << 2) | ((c3 & 0xC0) >> 6));
            out += base64EncodeChars.charAt(c3 & 0x3F);
          }
          return out;
        }
        return base64Encode(str)
    }
    sandBox.base64.atob=function atob(str) {
        function base64Decode(str) {
          let base64DecodeChars = new Array(
            -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,
            -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,
            -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 62, -1, -1, -1, 63,
            52, 53, 54, 55, 56, 57, 58, 59, 60, 61, -1, -1, -1, -1, -1, -1,
            -1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15,
            16, 17, 18, 19, 20, 21, 22, 23, 24, 25, -1, -1, -1, -1, 63, -1,
            26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41,
            42, 43, 44, 45, 46, 47, 48, 49, 50, 51, -1, -1, -1, -1, -1, -1
          );
          let c1, c2, c3, c4;
          let i = 0, len = str.length, out = "";

          while (i < len) {
            do {
              c1 = base64DecodeChars[str.charCodeAt(i++) & 0xff];
            } while (i < len && c1 == -1);
            if (c1 == -1) break;

            do {
              c2 = base64DecodeChars[str.charCodeAt(i++) & 0xff];
            } while (i < len && c2 == -1);
            if (c2 == -1) break;

            out += String.fromCharCode((c1 << 2) | ((c2 & 0x30) >> 4));

            do {
              c3 = str.charCodeAt(i++) & 0xff;
              if (c3 == 61) return out;
              c3 = base64DecodeChars[c3];
            } while (i < len && c3 == -1);
            if (c3 == -1) break;

            out += String.fromCharCode(((c2 & 0XF) << 4) | ((c3 & 0x3C) >> 2));

            do {
              c4 = str.charCodeAt(i++) & 0xff;
              if (c4 == 61) return out;
              c4 = base64DecodeChars[c4];
            } while (i < len && c4 == -1);
            if (c4 == -1) break;

            out += String.fromCharCode(((c3 & 0x03) << 6) | c4);
          }
          return out;
        }
        return base64Decode(str)
    }
}()
