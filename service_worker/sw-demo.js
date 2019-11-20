if('serviceWorker' in navigator){
    window,addEventListener('load',function(){
        navigator,serviceWorker.register("static/sw-demo.js",{scope:'/static/'})  // 此地址为serviceworker的真正工作文件地址, scope是确定文件所影响的域
            .then(function (registration) {
                // console.log(registion.scope);
            })
            .catch(function(error){

            });
    });
}