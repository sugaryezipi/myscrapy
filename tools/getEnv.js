//脱环境脚本
getEnvCode=function (proto,instanceObj) {
    let code="";
    let protoName=proto.name;
    code+=`//${protoName}环境\r\n`
    code+=`${protoName}=function ${protoName}(){\r\n`
    try{
        new proto;
    }catch(e){
        code+=`\tsandBox.throwError('${e.name}','${e.message}')\r\n`
    }
    code+=`}\r\n`;
    code+=`sandBox.safeProto(${protoName},"${protoName}")\r\n`
    let protoObject=proto.prototype;
    let getProtoName=Object.getPrototypeOf(proto.prototype)[Symbol.toStringTag]
    if(getProtoName){
        code+=`Object.setPrototypeOf(${protoName}.prototype,${getProtoName}.prototype)\r\n`
    }
    for(const key in Object.getOwnPropertyDescriptors(proto)){
        if(key==="arguments"||key==="caller"||key==="length"||key==="name"||key==="prototype"){
            continue;
        }
        let descriptor=Object.getOwnPropertyDescriptor(proto,key)
        code+=`sandBox.defineProperty(${protoName},"${key}",{configurable:${descriptor.configurable},enumerable:${descriptor.enumerable},`
        if(descriptor.hasOwnProperty("writable")){
            code+=`writable:${descriptor.writable},`
        }
        if(descriptor.hasOwnProperty("value")){
            if(descriptor.value instanceof Object){
                if(typeof descriptor.value==='function'){
                    code+=`value:function ${descriptor.value.name}() {
                                return sandBox.dispatch("${protoName}_${descriptor.value.name}",this,arguments)
                            }`
                }else{
                    code+=`value:{}//需要特殊处理`
                }
            }else if(typeof descriptor.value ==="string"){
                code+=`value:'${descriptor.value}'}`
            }else if(typeof descriptor.value === 'symbol'){
                code+=`value:${descriptor.value.toString()}`
            }else{
                code+=`value:${descriptor.value}`
            }
        }
        if(descriptor.hasOwnProperty("get")){
            if(typeof descriptor.get ==="function"){
                let defaultValue;
                try{
                    defaultValue=descriptor.get.call(instanceObj)
                }catch(e){}
                if(defaultValue instanceof Object || typeof defaultValue ===undefined){
                    code+=`get:function () {
                                return sandBox.dispatch("${protoName}_${key}_get",this,arguments)
                            },`
                }else if(typeof defaultValue ==="string"){
                    code+=`get:function () {
                                return sandBox.dispatch("${protoName}_${key}_get",this,arguments,'${defaultValue}')
                            },`
                }else if(typeof defaultValue === 'symbol'){
                    code+=`get:function () {
                                return sandBox.dispatch("${protoName}_${key}_get",this,arguments,${defaultValue.toString()})
                            },`
                }else{
                    code+=`get:function () {
                                return sandBox.dispatch("${protoName}_${key}_get",this,arguments,${defaultValue})
                            },`
                }

            }else{
                code+=`get:undefined,`
            }
        }
        if(descriptor.hasOwnProperty("set")){
            if(typeof descriptor.set==="function"){
                code+=`set:function () {
                                return sandBox.dispatch("${protoName}_${key}_set",this,arguments)
                            }`
            }else{
                code+=`set:undefined`
            }
        }

        code+=`})\r\n`
    }
    //浏览器原型对象
    for(const key in Object.getOwnPropertyDescriptors(proto.prototype)){
        if(key==="constructor"){
            continue;
        }
        let descriptor=Object.getOwnPropertyDescriptor(proto.prototype,key)
        code+=`sandBox.defineProperty(${protoName}.prototype,"${key}",{configurable:${descriptor.configurable},enumerable:${descriptor.enumerable},`
        if(descriptor.hasOwnProperty("writable")){
            code+=`writable:${descriptor.writable},`
        }
        if(descriptor.hasOwnProperty("value")){
            if(descriptor.value instanceof Object){
                if(typeof descriptor.value==='function'){
                    code+=`value:function ${descriptor.value.name}() {
                                return sandBox.dispatch("${protoName}_${descriptor.value.name}",this,arguments)
                            }`
                }else{
                    code+=`value:{}//需要特殊处理`
                }
            }else if(typeof descriptor.value ==="string"){
                code+=`value:'${descriptor.value}'}`
            }else if(typeof descriptor.value === 'symbol'){
                code+=`value:${descriptor.value.toString()}`
            }else{
                code+=`value:${descriptor.value}`
            }
        }
        if(descriptor.hasOwnProperty("get")){
            if(typeof descriptor.get ==="function"){
                let defaultValue;
                try{
                    defaultValue=descriptor.get.call(instanceObj)
                }catch(e){}
                if(defaultValue instanceof Object || typeof defaultValue ===undefined){
                    code+=`get:function () {
                                return sandBox.dispatch("${protoName}_${key}_get",this,arguments)
                            },`
                }else if(typeof defaultValue ==="string"){
                    code+=`get:function () {
                                return sandBox.dispatch("${protoName}_${key}_get",this,arguments,'${defaultValue}')
                            },`
                }else if(typeof defaultValue === 'symbol'){
                    code+=`get:function () {
                                return sandBox.dispatch("${protoName}_${key}_get",this,arguments,${defaultValue.toString()})
                            },`
                }else{
                    code+=`get:function () {
                                return sandBox.dispatch("${protoName}_${key}_get",this,arguments,${defaultValue})
                            },`
                }

            }else{
                code+=`get:undefined,`
            }
        }
        if(descriptor.hasOwnProperty("set")){
            if(typeof descriptor.set==="function"){
                code+=`set:function () {
                                return sandBox.dispatch("${protoName}_${key}_set",this,arguments)
                            }`
            }else{
                code+=`set:undefined`
            }
        }

        code+=`})\r\n`
    }
    console.log(code);
    copy(code);
    return code;
}


//脱实例对象
getObjEnvCode=function(obj,objName,instanceObj){
    let code="";
    code+=`//${objName}环境\r\n`
    code+=`${objName}={}\r\n`
    let getProtoName=Object.getPrototypeOf(obj)[Symbol.toStringTag]
    if(getProtoName){
        code+=`Object.setPrototypeOf(${objName},${getProtoName}.prototype)\r\n`
    }
    for(const key in Object.getOwnPropertyDescriptors(obj)){
        let descriptor=Object.getOwnPropertyDescriptor(obj,key)
        code+=`sandBox.defineProperty(${objName},"${key}",{configurable:${descriptor.configurable},enumerable:${descriptor.enumerable},`
        if(descriptor.hasOwnProperty("writable")){
            code+=`writable:${descriptor.writable},`
        }
        if(descriptor.hasOwnProperty("value")){
            if(descriptor.value instanceof Object){
                if(typeof descriptor.value==='function'){
                    code+=`value:function ${descriptor.value.name}() {
                                return sandBox.dispatch("${objName}_${descriptor.value.name}",this,arguments)
                            }`
                }else{
                    console.log('//需要特殊处理')
                    code+=`value:{}`
                }
            }else if(typeof descriptor.value ==="string"){
                code+=`value:'${descriptor.value}'`
            }else if(typeof descriptor.value === 'symbol'){
                code+=`value:${descriptor.value.toString()}`
            }else{
                try{
                    code+=`value:${descriptor.value}`
                }catch(e){
                    code+=`value:${JSON.stringify(descriptor.value)}`
                }

            }
        }
        if(descriptor.hasOwnProperty("get")){
            if(typeof descriptor.get ==="function"){
                let defaultValue;
                try{
                    defaultValue=descriptor.get.call(instanceObj)
                }catch(e){}
                if(defaultValue instanceof Object || typeof defaultValue ===undefined){
                    code+=`get:function () {
                                return sandBox.dispatch("${objName}_${key}_get",this,arguments)
                            },`
                }else if(typeof defaultValue ==="string"){
                    code+=`get:function () {
                                return sandBox.dispatch("${objName}_${key}_get",this,arguments,'${defaultValue}')
                            },`
                }else if(typeof defaultValue === 'symbol'){
                    code+=`get:function () {
                                return sandBox.dispatch("${objName}_${key}_get",this,arguments,${defaultValue.toString()})
                            },`
                }else{
                    code+=`get:function () {
                                return sandBox.dispatch("${objName}_${key}_get",this,arguments,${defaultValue})
                            },`
                }

            }else{
                code+=`get:undefined,`
            }
        }
        if(descriptor.hasOwnProperty("set")){
            if(typeof descriptor.set==="function"){
                code+=`set:function () {
                                return sandBox.dispatch("${objName}_${key}_set",this,arguments)
                            }`
            }else{
                code+=`set:undefined`
            }
        }

        code+=`})\r\n`
    }
    console.log(code);
    return code;
}