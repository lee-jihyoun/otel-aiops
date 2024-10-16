
# URL 에 올바르지 않은 값 입력
## 정상 URL : http://100.83.227.59/api/board/questions?workYn=true&order=create&page=0&size=10
## 오류 URL : http://localhost:8090/board/questions?workYn=true&order=delete&page=0&size=10

## 변경된 값 :
order=create -> order=delete

## 오류 메시지
	=====================================================================
	2024-10-14 23:36:05.535 ERROR 125064 --- [nio-8090-exec-5] c.k.d.c.e.h.GlobalExceptionHandler       : Caught RE
	java.lang.RuntimeException: Invalid order. Using create || like
		at com.ktds.dsquare.board.paging.PagingService.orderPage(PagingService.java:18) ~[main/:na]
		at com.ktds.dsquare.board.qna.service.QuestionService.getQuestions(QuestionService.java:91) ~[main/:na]
		at com.ktds.dsquare.board.qna.service.QuestionService$$FastClassBySpringCGLIB$$89be5eae.invoke(<generated>) ~[main/:na]
		at org.springframework.cglib.proxy.MethodProxy.invoke(MethodProxy.java:218) ~[spring-core-5.3.25.jar:5.3.25]
		at org.springframework.aop.framework.CglibAopProxy$CglibMethodInvocation.invokeJoinpoint(CglibAopProxy.java:793) ~[spring-aop-5.3.25.jar:5.3.25]
		at org.springframework.aop.framework.ReflectiveMethodInvocation.proceed(ReflectiveMethodInvocation.java:163) ~[spring-aop-5.3.25.jar:5.3.25]
		at org.springframework.aop.framework.CglibAopProxy$CglibMethodInvocation.proceed(CglibAopProxy.java:763) ~[spring-aop-5.3.25.jar:5.3.25]
		at org.springframework.aop.interceptor.ExposeInvocationInterceptor.invoke(ExposeInvocationInterceptor.java:97) ~[spring-aop-5.3.25.jar:5.3.25]
		at org.springframework.aop.framework.ReflectiveMethodInvocation.proceed(ReflectiveMethodInvocation.java:186) ~[spring-aop-5.3.25.jar:5.3.25]
		at org.springframework.aop.framework.CglibAopProxy$CglibMethodInvocation.proceed(CglibAopProxy.java:763) ~[spring-aop-5.3.25.jar:5.3.25]
		at org.springframework.aop.framework.CglibAopProxy$DynamicAdvisedInterceptor.intercept(CglibAopProxy.java:708) ~[spring-aop-5.3.25.jar:5.3.25]
		at com.ktds.dsquare.board.qna.service.QuestionService$$EnhancerBySpringCGLIB$$507c0ebb.getQuestions(<generated>) ~[main/:na]
		at com.ktds.dsquare.board.qna.controller.QuestionController.getQuestions(QuestionController.java:43) ~[main/:na]
		at java.base/jdk.internal.reflect.NativeMethodAccessorImpl.invoke0(Native Method) ~[na:na]
		at java.base/jdk.internal.reflect.NativeMethodAccessorImpl.invoke(NativeMethodAccessorImpl.java:77) ~[na:na]
		at java.base/jdk.internal.reflect.DelegatingMethodAccessorImpl.invoke(DelegatingMethodAccessorImpl.java:43) ~[na:na]
		at java.base/java.lang.reflect.Method.invoke(Method.java:568) ~[na:na]
		at org.springframework.web.method.support.InvocableHandlerMethod.doInvoke(InvocableHandlerMethod.java:205) ~[spring-web-5.3.25.jar:5.3.25]
		at org.springframework.web.method.support.InvocableHandlerMethod.invokeForRequest(InvocableHandlerMethod.java:150) ~[spring-web-5.3.25.jar:5.3.25]
		at org.springframework.web.servlet.mvc.method.annotation.ServletInvocableHandlerMethod.invokeAndHandle(ServletInvocableHandlerMethod.java:117) ~[spring-webmvc-5.3.25.jar:5.3.25]
		at org.springframework.web.servlet.mvc.method.annotation.RequestMappingHandlerAdapter.invokeHandlerMethod(RequestMappingHandlerAdapter.java:895) ~[spring-webmvc-5.3.25.jar:5.3.25]
		at org.springframework.web.servlet.mvc.method.annotation.RequestMappingHandlerAdapter.handleInternal(RequestMappingHandlerAdapter.java:808) ~[spring-webmvc-5.3.25.jar:5.3.25]
		at org.springframework.web.servlet.mvc.method.AbstractHandlerMethodAdapter.handle(AbstractHandlerMethodAdapter.java:87) ~[spring-webmvc-5.3.25.jar:5.3.25]
		at org.springframework.web.servlet.DispatcherServlet.doDispatch(DispatcherServlet.java:1071) ~[spring-webmvc-5.3.25.jar:5.3.25]
		at org.springframework.web.servlet.DispatcherServlet.doService(DispatcherServlet.java:964) ~[spring-webmvc-5.3.25.jar:5.3.25]
		at org.springframework.web.servlet.FrameworkServlet.processRequest(FrameworkServlet.java:1006) ~[spring-webmvc-5.3.25.jar:5.3.25]
		at org.springframework.web.servlet.FrameworkServlet.doGet(FrameworkServlet.java:898) ~[spring-webmvc-5.3.25.jar:5.3.25]
		at javax.servlet.http.HttpServlet.service(HttpServlet.java:670) ~[tomcat-embed-core-9.0.71.jar:4.0.FR]
		at org.springframework.web.servlet.FrameworkServlet.service(FrameworkServlet.java:883) ~[spring-webmvc-5.3.25.jar:5.3.25]
		at javax.servlet.http.HttpServlet.service(HttpServlet.java:779) ~[tomcat-embed-core-9.0.71.jar:4.0.FR]
		at org.apache.catalina.core.ApplicationFilterChain.internalDoFilter(ApplicationFilterChain.java:227) ~[tomcat-embed-core-9.0.71.jar:9.0.71]
		at org.apache.catalina.core.ApplicationFilterChain.doFilter(ApplicationFilterChain.java:162) ~[tomcat-embed-core-9.0.71.jar:9.0.71]
		at org.apache.tomcat.websocket.server.WsFilter.doFilter(WsFilter.java:53) ~[tomcat-embed-websocket-9.0.71.jar:9.0.71]
		at org.apache.catalina.core.ApplicationFilterChain.internalDoFilter(ApplicationFilterChain.java:189) ~[tomcat-embed-core-9.0.71.jar:9.0.71]
		at org.apache.catalina.core.ApplicationFilterChain.doFilter(ApplicationFilterChain.java:162) ~[tomcat-embed-core-9.0.71.jar:9.0.71]
		at org.springframework.security.web.FilterChainProxy$VirtualFilterChain.doFilter(FilterChainProxy.java:337) ~[spring-security-web-5.7.7.jar:5.7.7]
		at org.springframework.security.web.access.intercept.FilterSecurityInterceptor.invoke(FilterSecurityInterceptor.java:115) ~[spring-security-web-5.7.7.jar:5.7.7]
		at org.springframework.security.web.access.intercept.FilterSecurityInterceptor.doFilter(FilterSecurityInterceptor.java:81) ~[spring-security-web-5.7.7.jar:5.7.7]
		at org.springframework.security.web.FilterChainProxy$VirtualFilterChain.doFilter(FilterChainProxy.java:346) ~[spring-security-web-5.7.7.jar:5.7.7]
		at org.springframework.security.web.access.ExceptionTranslationFilter.doFilter(ExceptionTranslationFilter.java:122) ~[spring-security-web-5.7.7.jar:5.7.7]
		at org.springframework.security.web.access.ExceptionTranslationFilter.doFilter(ExceptionTranslationFilter.java:116) ~[spring-security-web-5.7.7.jar:5.7.7]
		at org.springframework.security.web.FilterChainProxy$VirtualFilterChain.doFilter(FilterChainProxy.java:346) ~[spring-security-web-5.7.7.jar:5.7.7]
		at org.springframework.security.web.session.SessionManagementFilter.doFilter(SessionManagementFilter.java:126) ~[spring-security-web-5.7.7.jar:5.7.7]
		at org.springframework.security.web.session.SessionManagementFilter.doFilter(SessionManagementFilter.java:81) ~[spring-security-web-5.7.7.jar:5.7.7]
		at org.springframework.security.web.FilterChainProxy$VirtualFilterChain.doFilter(FilterChainProxy.java:346) ~[spring-security-web-5.7.7.jar:5.7.7]
		at org.springframework.security.web.authentication.AnonymousAuthenticationFilter.doFilter(AnonymousAuthenticationFilter.java:109) ~[spring-security-web-5.7.7.jar:5.7.7]
		at org.springframework.security.web.FilterChainProxy$VirtualFilterChain.doFilter(FilterChainProxy.java:346) ~[spring-security-web-5.7.7.jar:5.7.7]
		at org.springframework.security.web.servletapi.SecurityContextHolderAwareRequestFilter.doFilter(SecurityContextHolderAwareRequestFilter.java:149) ~[spring-security-web-5.7.7.jar:5.7.7]
		at org.springframework.security.web.FilterChainProxy$VirtualFilterChain.doFilter(FilterChainProxy.java:346) ~[spring-security-web-5.7.7.jar:5.7.7]
		at org.springframework.security.web.savedrequest.RequestCacheAwareFilter.doFilter(RequestCacheAwareFilter.java:63) ~[spring-security-web-5.7.7.jar:5.7.7]
		at org.springframework.security.web.FilterChainProxy$VirtualFilterChain.doFilter(FilterChainProxy.java:346) ~[spring-security-web-5.7.7.jar:5.7.7]
		at com.ktds.dsquare.auth.filter.AuthenticationAuthorizationFilter.doFilterInternal(AuthenticationAuthorizationFilter.java:63) ~[main/:na]
		at org.springframework.web.filter.OncePerRequestFilter.doFilter(OncePerRequestFilter.java:117) ~[spring-web-5.3.25.jar:5.3.25]
		at org.springframework.security.web.FilterChainProxy$VirtualFilterChain.doFilter(FilterChainProxy.java:346) ~[spring-security-web-5.7.7.jar:5.7.7]
		at org.springframework.security.web.authentication.AbstractAuthenticationProcessingFilter.doFilter(AbstractAuthenticationProcessingFilter.java:223) ~[spring-security-web-5.7.7.jar:5.7.7]
		at org.springframework.security.web.authentication.AbstractAuthenticationProcessingFilter.doFilter(AbstractAuthenticationProcessingFilter.java:217) ~[spring-security-web-5.7.7.jar:5.7.7]
		at org.springframework.security.web.FilterChainProxy$VirtualFilterChain.doFilter(FilterChainProxy.java:346) ~[spring-security-web-5.7.7.jar:5.7.7]
		at org.springframework.security.web.authentication.logout.LogoutFilter.doFilter(LogoutFilter.java:103) ~[spring-security-web-5.7.7.jar:5.7.7]
		at org.springframework.security.web.authentication.logout.LogoutFilter.doFilter(LogoutFilter.java:89) ~[spring-security-web-5.7.7.jar:5.7.7]
		at org.springframework.security.web.FilterChainProxy$VirtualFilterChain.doFilter(FilterChainProxy.java:346) ~[spring-security-web-5.7.7.jar:5.7.7]
		at org.springframework.web.filter.CorsFilter.doFilterInternal(CorsFilter.java:91) ~[spring-web-5.3.25.jar:5.3.25]
		at org.springframework.web.filter.OncePerRequestFilter.doFilter(OncePerRequestFilter.java:117) ~[spring-web-5.3.25.jar:5.3.25]
		at org.springframework.security.web.FilterChainProxy$VirtualFilterChain.doFilter(FilterChainProxy.java:346) ~[spring-security-web-5.7.7.jar:5.7.7]
		at org.springframework.security.web.header.HeaderWriterFilter.doHeadersAfter(HeaderWriterFilter.java:90) ~[spring-security-web-5.7.7.jar:5.7.7]
		at org.springframework.security.web.header.HeaderWriterFilter.doFilterInternal(HeaderWriterFilter.java:75) ~[spring-security-web-5.7.7.jar:5.7.7]
		at org.springframework.web.filter.OncePerRequestFilter.doFilter(OncePerRequestFilter.java:117) ~[spring-web-5.3.25.jar:5.3.25]
		at org.springframework.security.web.FilterChainProxy$VirtualFilterChain.doFilter(FilterChainProxy.java:346) ~[spring-security-web-5.7.7.jar:5.7.7]
		at org.springframework.security.web.context.SecurityContextPersistenceFilter.doFilter(SecurityContextPersistenceFilter.java:112) ~[spring-security-web-5.7.7.jar:5.7.7]
		at org.springframework.security.web.context.SecurityContextPersistenceFilter.doFilter(SecurityContextPersistenceFilter.java:82) ~[spring-security-web-5.7.7.jar:5.7.7]
		at org.springframework.security.web.FilterChainProxy$VirtualFilterChain.doFilter(FilterChainProxy.java:346) ~[spring-security-web-5.7.7.jar:5.7.7]
		at org.springframework.security.web.context.request.async.WebAsyncManagerIntegrationFilter.doFilterInternal(WebAsyncManagerIntegrationFilter.java:55) ~[spring-security-web-5.7.7.jar:5.7.7]
		at org.springframework.web.filter.OncePerRequestFilter.doFilter(OncePerRequestFilter.java:117) ~[spring-web-5.3.25.jar:5.3.25]
		at org.springframework.security.web.FilterChainProxy$VirtualFilterChain.doFilter(FilterChainProxy.java:346) ~[spring-security-web-5.7.7.jar:5.7.7]
		at org.springframework.security.web.session.DisableEncodeUrlFilter.doFilterInternal(DisableEncodeUrlFilter.java:42) ~[spring-security-web-5.7.7.jar:5.7.7]
		at org.springframework.web.filter.OncePerRequestFilter.doFilter(OncePerRequestFilter.java:117) ~[spring-web-5.3.25.jar:5.3.25]
		at org.springframework.security.web.FilterChainProxy$VirtualFilterChain.doFilter(FilterChainProxy.java:346) ~[spring-security-web-5.7.7.jar:5.7.7]
		at org.springframework.security.web.FilterChainProxy.doFilterInternal(FilterChainProxy.java:221) ~[spring-security-web-5.7.7.jar:5.7.7]
		at org.springframework.security.web.FilterChainProxy.doFilter(FilterChainProxy.java:186) ~[spring-security-web-5.7.7.jar:5.7.7]
		at org.springframework.web.filter.DelegatingFilterProxy.invokeDelegate(DelegatingFilterProxy.java:354) ~[spring-web-5.3.25.jar:5.3.25]
		at org.springframework.web.filter.DelegatingFilterProxy.doFilter(DelegatingFilterProxy.java:267) ~[spring-web-5.3.25.jar:5.3.25]
		at org.apache.catalina.core.ApplicationFilterChain.internalDoFilter(ApplicationFilterChain.java:189) ~[tomcat-embed-core-9.0.71.jar:9.0.71]
		at org.apache.catalina.core.ApplicationFilterChain.doFilter(ApplicationFilterChain.java:162) ~[tomcat-embed-core-9.0.71.jar:9.0.71]
		at org.springframework.web.filter.CharacterEncodingFilter.doFilterInternal(CharacterEncodingFilter.java:201) ~[spring-web-5.3.25.jar:5.3.25]
		at org.springframework.web.filter.OncePerRequestFilter.doFilter(OncePerRequestFilter.java:117) ~[spring-web-5.3.25.jar:5.3.25]
		at org.apache.catalina.core.ApplicationFilterChain.internalDoFilter(ApplicationFilterChain.java:189) ~[tomcat-embed-core-9.0.71.jar:9.0.71]
		at org.apache.catalina.core.ApplicationFilterChain.doFilter(ApplicationFilterChain.java:162) ~[tomcat-embed-core-9.0.71.jar:9.0.71]
		at org.apache.catalina.core.StandardWrapperValve.invoke(StandardWrapperValve.java:177) ~[tomcat-embed-core-9.0.71.jar:9.0.71]
		at org.apache.catalina.core.StandardContextValve.invoke(StandardContextValve.java:97) ~[tomcat-embed-core-9.0.71.jar:9.0.71]
		at org.apache.catalina.authenticator.AuthenticatorBase.invoke(AuthenticatorBase.java:541) ~[tomcat-embed-core-9.0.71.jar:9.0.71]
		at org.apache.catalina.core.StandardHostValve.invoke(StandardHostValve.java:135) ~[tomcat-embed-core-9.0.71.jar:9.0.71]
		at org.apache.catalina.valves.ErrorReportValve.invoke(ErrorReportValve.java:92) ~[tomcat-embed-core-9.0.71.jar:9.0.71]
		at org.apache.catalina.core.StandardEngineValve.invoke(StandardEngineValve.java:78) ~[tomcat-embed-core-9.0.71.jar:9.0.71]
		at org.apache.catalina.connector.CoyoteAdapter.service(CoyoteAdapter.java:360) ~[tomcat-embed-core-9.0.71.jar:9.0.71]
		at org.apache.coyote.http11.Http11Processor.service(Http11Processor.java:399) ~[tomcat-embed-core-9.0.71.jar:9.0.71]
		at org.apache.coyote.AbstractProcessorLight.process(AbstractProcessorLight.java:65) ~[tomcat-embed-core-9.0.71.jar:9.0.71]
		at org.apache.coyote.AbstractProtocol$ConnectionHandler.process(AbstractProtocol.java:891) ~[tomcat-embed-core-9.0.71.jar:9.0.71]
		at org.apache.tomcat.util.net.NioEndpoint$SocketProcessor.doRun(NioEndpoint.java:1784) ~[tomcat-embed-core-9.0.71.jar:9.0.71]
		at org.apache.tomcat.util.net.SocketProcessorBase.run(SocketProcessorBase.java:49) ~[tomcat-embed-core-9.0.71.jar:9.0.71]
		at org.apache.tomcat.util.threads.ThreadPoolExecutor.runWorker(ThreadPoolExecutor.java:1191) ~[tomcat-embed-core-9.0.71.jar:9.0.71]
		at org.apache.tomcat.util.threads.ThreadPoolExecutor$Worker.run(ThreadPoolExecutor.java:659) ~[tomcat-embed-core-9.0.71.jar:9.0.71]
		at org.apache.tomcat.util.threads.TaskThread$WrappingRunnable.run(TaskThread.java:61) ~[tomcat-embed-core-9.0.71.jar:9.0.71]
		at java.base/java.lang.Thread.run(Thread.java:833) ~[na:na]
		=====================================================================

## 오류 원인
	if 문에서 order의 값이 create나 like가 아닐경우 RuntimeException 으로 오류 던짐
	=====================================================================
    public Pageable orderPage(String order, Pageable pageable){
        Pageable page;
        if(order == null || order.equals("create")){
            page = PageRequest.of(pageable.getPageNumber(), pageable.getPageSize(), Sort.by("createDate").descending());
        } else if (order.equals("like")) {
            page = PageRequest.of(pageable.getPageNumber(), pageable.getPageSize(), Sort.by("likeCnt", "createDate").descending());
        } else {
            throw new RuntimeException("Invalid order. Using create || like");
        }
        return page;
    }
	=====================================================================




# URL 에 올바르지 않은 값 입력
## 정상 URL : http://100.83.227.59/api/board/talks?order=create&page=0&size=10
## 오류 URL : http://100.83.227.59/api/board/talks?order=aaaa&page=0&size=10

## 변경된 값 :
order=create -> order=aaaa

## 오류 메시지
	=====================================================================
	2024-10-14 23:36:05.535 ERROR 125064 --- [nio-8090-exec-5] c.k.d.c.e.h.GlobalExceptionHandler       : Caught RE
	java.lang.RuntimeException: Invalid order. Using create || like
		at com.ktds.dsquare.board.paging.PagingService.orderPage(PagingService.java:18) ~[main/:na]
		at com.ktds.dsquare.board.qna.service.QuestionService.getQuestions(QuestionService.java:91) ~[main/:na]
		at com.ktds.dsquare.board.qna.service.QuestionService$$FastClassBySpringCGLIB$$89be5eae.invoke(<generated>) ~[main/:na]
		at org.springframework.cglib.proxy.MethodProxy.invoke(MethodProxy.java:218) ~[spring-core-5.3.25.jar:5.3.25]
		at org.springframework.aop.framework.CglibAopProxy$CglibMethodInvocation.invokeJoinpoint(CglibAopProxy.java:793) ~[spring-aop-5.3.25.jar:5.3.25]
		at org.springframework.aop.framework.ReflectiveMethodInvocation.proceed(ReflectiveMethodInvocation.java:163) ~[spring-aop-5.3.25.jar:5.3.25]
		at org.springframework.aop.framework.CglibAopProxy$CglibMethodInvocation.proceed(CglibAopProxy.java:763) ~[spring-aop-5.3.25.jar:5.3.25]
		at org.springframework.aop.interceptor.ExposeInvocationInterceptor.invoke(ExposeInvocationInterceptor.java:97) ~[spring-aop-5.3.25.jar:5.3.25]
		at org.springframework.aop.framework.ReflectiveMethodInvocation.proceed(ReflectiveMethodInvocation.java:186) ~[spring-aop-5.3.25.jar:5.3.25]
		at org.springframework.aop.framework.CglibAopProxy$CglibMethodInvocation.proceed(CglibAopProxy.java:763) ~[spring-aop-5.3.25.jar:5.3.25]
		at org.springframework.aop.framework.CglibAopProxy$DynamicAdvisedInterceptor.intercept(CglibAopProxy.java:708) ~[spring-aop-5.3.25.jar:5.3.25]
		at com.ktds.dsquare.board.qna.service.QuestionService$$EnhancerBySpringCGLIB$$507c0ebb.getQuestions(<generated>) ~[main/:na]
		at com.ktds.dsquare.board.qna.controller.QuestionController.getQuestions(QuestionController.java:43) ~[main/:na]
		at java.base/jdk.internal.reflect.NativeMethodAccessorImpl.invoke0(Native Method) ~[na:na]
		at java.base/jdk.internal.reflect.NativeMethodAccessorImpl.invoke(NativeMethodAccessorImpl.java:77) ~[na:na]
		at java.base/jdk.internal.reflect.DelegatingMethodAccessorImpl.invoke(DelegatingMethodAccessorImpl.java:43) ~[na:na]
		at java.base/java.lang.reflect.Method.invoke(Method.java:568) ~[na:na]
		at org.springframework.web.method.support.InvocableHandlerMethod.doInvoke(InvocableHandlerMethod.java:205) ~[spring-web-5.3.25.jar:5.3.25]
		at org.springframework.web.method.support.InvocableHandlerMethod.invokeForRequest(InvocableHandlerMethod.java:150) ~[spring-web-5.3.25.jar:5.3.25]
		at org.springframework.web.servlet.mvc.method.annotation.ServletInvocableHandlerMethod.invokeAndHandle(ServletInvocableHandlerMethod.java:117) ~[spring-webmvc-5.3.25.jar:5.3.25]
		at org.springframework.web.servlet.mvc.method.annotation.RequestMappingHandlerAdapter.invokeHandlerMethod(RequestMappingHandlerAdapter.java:895) ~[spring-webmvc-5.3.25.jar:5.3.25]
		at org.springframework.web.servlet.mvc.method.annotation.RequestMappingHandlerAdapter.handleInternal(RequestMappingHandlerAdapter.java:808) ~[spring-webmvc-5.3.25.jar:5.3.25]
		at org.springframework.web.servlet.mvc.method.AbstractHandlerMethodAdapter.handle(AbstractHandlerMethodAdapter.java:87) ~[spring-webmvc-5.3.25.jar:5.3.25]
		at org.springframework.web.servlet.DispatcherServlet.doDispatch(DispatcherServlet.java:1071) ~[spring-webmvc-5.3.25.jar:5.3.25]
		at org.springframework.web.servlet.DispatcherServlet.doService(DispatcherServlet.java:964) ~[spring-webmvc-5.3.25.jar:5.3.25]
		at org.springframework.web.servlet.FrameworkServlet.processRequest(FrameworkServlet.java:1006) ~[spring-webmvc-5.3.25.jar:5.3.25]
		at org.springframework.web.servlet.FrameworkServlet.doGet(FrameworkServlet.java:898) ~[spring-webmvc-5.3.25.jar:5.3.25]
		at javax.servlet.http.HttpServlet.service(HttpServlet.java:670) ~[tomcat-embed-core-9.0.71.jar:4.0.FR]
		at org.springframework.web.servlet.FrameworkServlet.service(FrameworkServlet.java:883) ~[spring-webmvc-5.3.25.jar:5.3.25]
		at javax.servlet.http.HttpServlet.service(HttpServlet.java:779) ~[tomcat-embed-core-9.0.71.jar:4.0.FR]
		at org.apache.catalina.core.ApplicationFilterChain.internalDoFilter(ApplicationFilterChain.java:227) ~[tomcat-embed-core-9.0.71.jar:9.0.71]
		at org.apache.catalina.core.ApplicationFilterChain.doFilter(ApplicationFilterChain.java:162) ~[tomcat-embed-core-9.0.71.jar:9.0.71]
		at org.apache.tomcat.websocket.server.WsFilter.doFilter(WsFilter.java:53) ~[tomcat-embed-websocket-9.0.71.jar:9.0.71]
		at org.apache.catalina.core.ApplicationFilterChain.internalDoFilter(ApplicationFilterChain.java:189) ~[tomcat-embed-core-9.0.71.jar:9.0.71]
		at org.apache.catalina.core.ApplicationFilterChain.doFilter(ApplicationFilterChain.java:162) ~[tomcat-embed-core-9.0.71.jar:9.0.71]
		at org.springframework.security.web.FilterChainProxy$VirtualFilterChain.doFilter(FilterChainProxy.java:337) ~[spring-security-web-5.7.7.jar:5.7.7]
		at org.springframework.security.web.access.intercept.FilterSecurityInterceptor.invoke(FilterSecurityInterceptor.java:115) ~[spring-security-web-5.7.7.jar:5.7.7]
		at org.springframework.security.web.access.intercept.FilterSecurityInterceptor.doFilter(FilterSecurityInterceptor.java:81) ~[spring-security-web-5.7.7.jar:5.7.7]
		at org.springframework.security.web.FilterChainProxy$VirtualFilterChain.doFilter(FilterChainProxy.java:346) ~[spring-security-web-5.7.7.jar:5.7.7]
		at org.springframework.security.web.access.ExceptionTranslationFilter.doFilter(ExceptionTranslationFilter.java:122) ~[spring-security-web-5.7.7.jar:5.7.7]
		at org.springframework.security.web.access.ExceptionTranslationFilter.doFilter(ExceptionTranslationFilter.java:116) ~[spring-security-web-5.7.7.jar:5.7.7]
		at org.springframework.security.web.FilterChainProxy$VirtualFilterChain.doFilter(FilterChainProxy.java:346) ~[spring-security-web-5.7.7.jar:5.7.7]
		at org.springframework.security.web.session.SessionManagementFilter.doFilter(SessionManagementFilter.java:126) ~[spring-security-web-5.7.7.jar:5.7.7]
		at org.springframework.security.web.session.SessionManagementFilter.doFilter(SessionManagementFilter.java:81) ~[spring-security-web-5.7.7.jar:5.7.7]
		at org.springframework.security.web.FilterChainProxy$VirtualFilterChain.doFilter(FilterChainProxy.java:346) ~[spring-security-web-5.7.7.jar:5.7.7]
		at org.springframework.security.web.authentication.AnonymousAuthenticationFilter.doFilter(AnonymousAuthenticationFilter.java:109) ~[spring-security-web-5.7.7.jar:5.7.7]
		at org.springframework.security.web.FilterChainProxy$VirtualFilterChain.doFilter(FilterChainProxy.java:346) ~[spring-security-web-5.7.7.jar:5.7.7]
		at org.springframework.security.web.servletapi.SecurityContextHolderAwareRequestFilter.doFilter(SecurityContextHolderAwareRequestFilter.java:149) ~[spring-security-web-5.7.7.jar:5.7.7]
		at org.springframework.security.web.FilterChainProxy$VirtualFilterChain.doFilter(FilterChainProxy.java:346) ~[spring-security-web-5.7.7.jar:5.7.7]
		at org.springframework.security.web.savedrequest.RequestCacheAwareFilter.doFilter(RequestCacheAwareFilter.java:63) ~[spring-security-web-5.7.7.jar:5.7.7]
		at org.springframework.security.web.FilterChainProxy$VirtualFilterChain.doFilter(FilterChainProxy.java:346) ~[spring-security-web-5.7.7.jar:5.7.7]
		at com.ktds.dsquare.auth.filter.AuthenticationAuthorizationFilter.doFilterInternal(AuthenticationAuthorizationFilter.java:63) ~[main/:na]
		at org.springframework.web.filter.OncePerRequestFilter.doFilter(OncePerRequestFilter.java:117) ~[spring-web-5.3.25.jar:5.3.25]
		at org.springframework.security.web.FilterChainProxy$VirtualFilterChain.doFilter(FilterChainProxy.java:346) ~[spring-security-web-5.7.7.jar:5.7.7]
		at org.springframework.security.web.authentication.AbstractAuthenticationProcessingFilter.doFilter(AbstractAuthenticationProcessingFilter.java:223) ~[spring-security-web-5.7.7.jar:5.7.7]
		at org.springframework.security.web.authentication.AbstractAuthenticationProcessingFilter.doFilter(AbstractAuthenticationProcessingFilter.java:217) ~[spring-security-web-5.7.7.jar:5.7.7]
		at org.springframework.security.web.FilterChainProxy$VirtualFilterChain.doFilter(FilterChainProxy.java:346) ~[spring-security-web-5.7.7.jar:5.7.7]
		at org.springframework.security.web.authentication.logout.LogoutFilter.doFilter(LogoutFilter.java:103) ~[spring-security-web-5.7.7.jar:5.7.7]
		at org.springframework.security.web.authentication.logout.LogoutFilter.doFilter(LogoutFilter.java:89) ~[spring-security-web-5.7.7.jar:5.7.7]
		at org.springframework.security.web.FilterChainProxy$VirtualFilterChain.doFilter(FilterChainProxy.java:346) ~[spring-security-web-5.7.7.jar:5.7.7]
		at org.springframework.web.filter.CorsFilter.doFilterInternal(CorsFilter.java:91) ~[spring-web-5.3.25.jar:5.3.25]
		at org.springframework.web.filter.OncePerRequestFilter.doFilter(OncePerRequestFilter.java:117) ~[spring-web-5.3.25.jar:5.3.25]
		at org.springframework.security.web.FilterChainProxy$VirtualFilterChain.doFilter(FilterChainProxy.java:346) ~[spring-security-web-5.7.7.jar:5.7.7]
		at org.springframework.security.web.header.HeaderWriterFilter.doHeadersAfter(HeaderWriterFilter.java:90) ~[spring-security-web-5.7.7.jar:5.7.7]
		at org.springframework.security.web.header.HeaderWriterFilter.doFilterInternal(HeaderWriterFilter.java:75) ~[spring-security-web-5.7.7.jar:5.7.7]
		at org.springframework.web.filter.OncePerRequestFilter.doFilter(OncePerRequestFilter.java:117) ~[spring-web-5.3.25.jar:5.3.25]
		at org.springframework.security.web.FilterChainProxy$VirtualFilterChain.doFilter(FilterChainProxy.java:346) ~[spring-security-web-5.7.7.jar:5.7.7]
		at org.springframework.security.web.context.SecurityContextPersistenceFilter.doFilter(SecurityContextPersistenceFilter.java:112) ~[spring-security-web-5.7.7.jar:5.7.7]
		at org.springframework.security.web.context.SecurityContextPersistenceFilter.doFilter(SecurityContextPersistenceFilter.java:82) ~[spring-security-web-5.7.7.jar:5.7.7]
		at org.springframework.security.web.FilterChainProxy$VirtualFilterChain.doFilter(FilterChainProxy.java:346) ~[spring-security-web-5.7.7.jar:5.7.7]
		at org.springframework.security.web.context.request.async.WebAsyncManagerIntegrationFilter.doFilterInternal(WebAsyncManagerIntegrationFilter.java:55) ~[spring-security-web-5.7.7.jar:5.7.7]
		at org.springframework.web.filter.OncePerRequestFilter.doFilter(OncePerRequestFilter.java:117) ~[spring-web-5.3.25.jar:5.3.25]
		at org.springframework.security.web.FilterChainProxy$VirtualFilterChain.doFilter(FilterChainProxy.java:346) ~[spring-security-web-5.7.7.jar:5.7.7]
		at org.springframework.security.web.session.DisableEncodeUrlFilter.doFilterInternal(DisableEncodeUrlFilter.java:42) ~[spring-security-web-5.7.7.jar:5.7.7]
		at org.springframework.web.filter.OncePerRequestFilter.doFilter(OncePerRequestFilter.java:117) ~[spring-web-5.3.25.jar:5.3.25]
		at org.springframework.security.web.FilterChainProxy$VirtualFilterChain.doFilter(FilterChainProxy.java:346) ~[spring-security-web-5.7.7.jar:5.7.7]
		at org.springframework.security.web.FilterChainProxy.doFilterInternal(FilterChainProxy.java:221) ~[spring-security-web-5.7.7.jar:5.7.7]
		at org.springframework.security.web.FilterChainProxy.doFilter(FilterChainProxy.java:186) ~[spring-security-web-5.7.7.jar:5.7.7]
		at org.springframework.web.filter.DelegatingFilterProxy.invokeDelegate(DelegatingFilterProxy.java:354) ~[spring-web-5.3.25.jar:5.3.25]
		at org.springframework.web.filter.DelegatingFilterProxy.doFilter(DelegatingFilterProxy.java:267) ~[spring-web-5.3.25.jar:5.3.25]
		at org.apache.catalina.core.ApplicationFilterChain.internalDoFilter(ApplicationFilterChain.java:189) ~[tomcat-embed-core-9.0.71.jar:9.0.71]
		at org.apache.catalina.core.ApplicationFilterChain.doFilter(ApplicationFilterChain.java:162) ~[tomcat-embed-core-9.0.71.jar:9.0.71]
		at org.springframework.web.filter.CharacterEncodingFilter.doFilterInternal(CharacterEncodingFilter.java:201) ~[spring-web-5.3.25.jar:5.3.25]
		at org.springframework.web.filter.OncePerRequestFilter.doFilter(OncePerRequestFilter.java:117) ~[spring-web-5.3.25.jar:5.3.25]
		at org.apache.catalina.core.ApplicationFilterChain.internalDoFilter(ApplicationFilterChain.java:189) ~[tomcat-embed-core-9.0.71.jar:9.0.71]
		at org.apache.catalina.core.ApplicationFilterChain.doFilter(ApplicationFilterChain.java:162) ~[tomcat-embed-core-9.0.71.jar:9.0.71]
		at org.apache.catalina.core.StandardWrapperValve.invoke(StandardWrapperValve.java:177) ~[tomcat-embed-core-9.0.71.jar:9.0.71]
		at org.apache.catalina.core.StandardContextValve.invoke(StandardContextValve.java:97) ~[tomcat-embed-core-9.0.71.jar:9.0.71]
		at org.apache.catalina.authenticator.AuthenticatorBase.invoke(AuthenticatorBase.java:541) ~[tomcat-embed-core-9.0.71.jar:9.0.71]
		at org.apache.catalina.core.StandardHostValve.invoke(StandardHostValve.java:135) ~[tomcat-embed-core-9.0.71.jar:9.0.71]
		at org.apache.catalina.valves.ErrorReportValve.invoke(ErrorReportValve.java:92) ~[tomcat-embed-core-9.0.71.jar:9.0.71]
		at org.apache.catalina.core.StandardEngineValve.invoke(StandardEngineValve.java:78) ~[tomcat-embed-core-9.0.71.jar:9.0.71]
		at org.apache.catalina.connector.CoyoteAdapter.service(CoyoteAdapter.java:360) ~[tomcat-embed-core-9.0.71.jar:9.0.71]
		at org.apache.coyote.http11.Http11Processor.service(Http11Processor.java:399) ~[tomcat-embed-core-9.0.71.jar:9.0.71]
		at org.apache.coyote.AbstractProcessorLight.process(AbstractProcessorLight.java:65) ~[tomcat-embed-core-9.0.71.jar:9.0.71]
		at org.apache.coyote.AbstractProtocol$ConnectionHandler.process(AbstractProtocol.java:891) ~[tomcat-embed-core-9.0.71.jar:9.0.71]
		at org.apache.tomcat.util.net.NioEndpoint$SocketProcessor.doRun(NioEndpoint.java:1784) ~[tomcat-embed-core-9.0.71.jar:9.0.71]
		at org.apache.tomcat.util.net.SocketProcessorBase.run(SocketProcessorBase.java:49) ~[tomcat-embed-core-9.0.71.jar:9.0.71]
		at org.apache.tomcat.util.threads.ThreadPoolExecutor.runWorker(ThreadPoolExecutor.java:1191) ~[tomcat-embed-core-9.0.71.jar:9.0.71]
		at org.apache.tomcat.util.threads.ThreadPoolExecutor$Worker.run(ThreadPoolExecutor.java:659) ~[tomcat-embed-core-9.0.71.jar:9.0.71]
		at org.apache.tomcat.util.threads.TaskThread$WrappingRunnable.run(TaskThread.java:61) ~[tomcat-embed-core-9.0.71.jar:9.0.71]
		at java.base/java.lang.Thread.run(Thread.java:833) ~[na:na]
		=====================================================================

## 오류 원인
	if 문에서 order의 값이 create나 like가 아닐경우 RuntimeException 으로 오류 던짐
	=====================================================================
    public Pageable orderPage(String order, Pageable pageable){
        Pageable page;
        if(order == null || order.equals("create")){
            page = PageRequest.of(pageable.getPageNumber(), pageable.getPageSize(), Sort.by("createDate").descending());
        } else if (order.equals("like")) {
            page = PageRequest.of(pageable.getPageNumber(), pageable.getPageSize(), Sort.by("likeCnt", "createDate").descending());
        } else {
            throw new RuntimeException("Invalid order. Using create || like");
        }
        return page;
    }
	=====================================================================

# 글 작성 시 제목에 길이 초과

## URL : http://localhost:8090/board/talks
## method : post
## data :
	{
		"content":"<p>aaaaaaaaa</p>",
		"title":"aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
		"tags":[],
		"atc":{"originFileName":"원본파일명","extension":"png","fileSize":51239}
	}
## 오류 메시지
	=====================================================================
	2024-10-15 01:51:47.523  WARN 125064 --- [nio-8090-exec-8] o.h.engine.jdbc.spi.SqlExceptionHelper   : SQL Error: 0, SQLState: 22001
	2024-10-15 01:51:47.523 ERROR 125064 --- [nio-8090-exec-8] o.h.engine.jdbc.spi.SqlExceptionHelper   : 오류: character varying(100) 자료형에 너무 긴 자료를 담으려고 합니다.
	2024-10-15 01:51:47.524  INFO 125064 --- [nio-8090-exec-8] o.h.e.j.b.internal.AbstractBatchImpl     : HHH000010: On release of batch it still contained JDBC statements
	2024-10-15 01:51:47.530 ERROR 125064 --- [nio-8090-exec-8] c.k.d.c.e.h.GlobalExceptionHandler       : Caught RE

	org.springframework.dao.DataIntegrityViolationException: could not execute statement; SQL [n/a]; nested exception is org.hibernate.exception.DataException: could not execute statement
		at org.springframework.orm.jpa.vendor.HibernateJpaDialect.convertHibernateAccessException(HibernateJpaDialect.java:280) ~[spring-orm-5.3.25.jar:5.3.25]
		at org.springframework.orm.jpa.vendor.HibernateJpaDialect.translateExceptionIfPossible(HibernateJpaDialect.java:233) ~[spring-orm-5.3.25.jar:5.3.25]
		at org.springframework.orm.jpa.JpaTransactionManager.doCommit(JpaTransactionManager.java:566) ~[spring-orm-5.3.25.jar:5.3.25]
		at org.springframework.transaction.support.AbstractPlatformTransactionManager.processCommit(AbstractPlatformTransactionManager.java:743) ~[spring-tx-5.3.25.jar:5.3.25]
		at org.springframework.transaction.support.AbstractPlatformTransactionManager.commit(AbstractPlatformTransactionManager.java:711) ~[spring-tx-5.3.25.jar:5.3.25]
		at org.springframework.transaction.interceptor.TransactionAspectSupport.commitTransactionAfterReturning(TransactionAspectSupport.java:654) ~[spring-tx-5.3.25.jar:5.3.25]
		at org.springframework.transaction.interceptor.TransactionAspectSupport.invokeWithinTransaction(TransactionAspectSupport.java:407) ~[spring-tx-5.3.25.jar:5.3.25]
		at org.springframework.transaction.interceptor.TransactionInterceptor.invoke(TransactionInterceptor.java:119) ~[spring-tx-5.3.25.jar:5.3.25]
		at org.springframework.aop.framework.ReflectiveMethodInvocation.proceed(ReflectiveMethodInvocation.java:186) ~[spring-aop-5.3.25.jar:5.3.25]
		at org.springframework.aop.framework.CglibAopProxy$CglibMethodInvocation.proceed(CglibAopProxy.java:763) ~[spring-aop-5.3.25.jar:5.3.25]
		at org.springframework.aop.framework.CglibAopProxy$DynamicAdvisedInterceptor.intercept(CglibAopProxy.java:708) ~[spring-aop-5.3.25.jar:5.3.25]
		at com.ktds.dsquare.board.talk.TalkService$$EnhancerBySpringCGLIB$$984b9917.createTalk(<generated>) ~[main/:na]
		at com.ktds.dsquare.board.talk.TalkController.createTalk(TalkController.java:28) ~[main/:na]
		at java.base/jdk.internal.reflect.NativeMethodAccessorImpl.invoke0(Native Method) ~[na:na]
		at java.base/jdk.internal.reflect.NativeMethodAccessorImpl.invoke(NativeMethodAccessorImpl.java:77) ~[na:na]
		at java.base/jdk.internal.reflect.DelegatingMethodAccessorImpl.invoke(DelegatingMethodAccessorImpl.java:43) ~[na:na]
		at java.base/java.lang.reflect.Method.invoke(Method.java:568) ~[na:na]
		at org.springframework.web.method.support.InvocableHandlerMethod.doInvoke(InvocableHandlerMethod.java:205) ~[spring-web-5.3.25.jar:5.3.25]
		at org.springframework.web.method.support.InvocableHandlerMethod.invokeForRequest(InvocableHandlerMethod.java:150) ~[spring-web-5.3.25.jar:5.3.25]
		at org.springframework.web.servlet.mvc.method.annotation.ServletInvocableHandlerMethod.invokeAndHandle(ServletInvocableHandlerMethod.java:117) ~[spring-webmvc-5.3.25.jar:5.3.25]
		at org.springframework.web.servlet.mvc.method.annotation.RequestMappingHandlerAdapter.invokeHandlerMethod(RequestMappingHandlerAdapter.java:895) ~[spring-webmvc-5.3.25.jar:5.3.25]
		at org.springframework.web.servlet.mvc.method.annotation.RequestMappingHandlerAdapter.handleInternal(RequestMappingHandlerAdapter.java:808) ~[spring-webmvc-5.3.25.jar:5.3.25]
		at org.springframework.web.servlet.mvc.method.AbstractHandlerMethodAdapter.handle(AbstractHandlerMethodAdapter.java:87) ~[spring-webmvc-5.3.25.jar:5.3.25]
		at org.springframework.web.servlet.DispatcherServlet.doDispatch(DispatcherServlet.java:1071) ~[spring-webmvc-5.3.25.jar:5.3.25]
		at org.springframework.web.servlet.DispatcherServlet.doService(DispatcherServlet.java:964) ~[spring-webmvc-5.3.25.jar:5.3.25]
		at org.springframework.web.servlet.FrameworkServlet.processRequest(FrameworkServlet.java:1006) ~[spring-webmvc-5.3.25.jar:5.3.25]
		at org.springframework.web.servlet.FrameworkServlet.doPost(FrameworkServlet.java:909) ~[spring-webmvc-5.3.25.jar:5.3.25]
		at javax.servlet.http.HttpServlet.service(HttpServlet.java:696) ~[tomcat-embed-core-9.0.71.jar:4.0.FR]
		at org.springframework.web.servlet.FrameworkServlet.service(FrameworkServlet.java:883) ~[spring-webmvc-5.3.25.jar:5.3.25]
		at javax.servlet.http.HttpServlet.service(HttpServlet.java:779) ~[tomcat-embed-core-9.0.71.jar:4.0.FR]
		at org.apache.catalina.core.ApplicationFilterChain.internalDoFilter(ApplicationFilterChain.java:227) ~[tomcat-embed-core-9.0.71.jar:9.0.71]
		at org.apache.catalina.core.ApplicationFilterChain.doFilter(ApplicationFilterChain.java:162) ~[tomcat-embed-core-9.0.71.jar:9.0.71]
		at org.apache.tomcat.websocket.server.WsFilter.doFilter(WsFilter.java:53) ~[tomcat-embed-websocket-9.0.71.jar:9.0.71]
		at org.apache.catalina.core.ApplicationFilterChain.internalDoFilter(ApplicationFilterChain.java:189) ~[tomcat-embed-core-9.0.71.jar:9.0.71]
		at org.apache.catalina.core.ApplicationFilterChain.doFilter(ApplicationFilterChain.java:162) ~[tomcat-embed-core-9.0.71.jar:9.0.71]
		at org.springframework.security.web.FilterChainProxy$VirtualFilterChain.doFilter(FilterChainProxy.java:337) ~[spring-security-web-5.7.7.jar:5.7.7]
		at org.springframework.security.web.access.intercept.FilterSecurityInterceptor.invoke(FilterSecurityInterceptor.java:115) ~[spring-security-web-5.7.7.jar:5.7.7]
		at org.springframework.security.web.access.intercept.FilterSecurityInterceptor.doFilter(FilterSecurityInterceptor.java:81) ~[spring-security-web-5.7.7.jar:5.7.7]
		at org.springframework.security.web.FilterChainProxy$VirtualFilterChain.doFilter(FilterChainProxy.java:346) ~[spring-security-web-5.7.7.jar:5.7.7]
		at org.springframework.security.web.access.ExceptionTranslationFilter.doFilter(ExceptionTranslationFilter.java:122) ~[spring-security-web-5.7.7.jar:5.7.7]
		at org.springframework.security.web.access.ExceptionTranslationFilter.doFilter(ExceptionTranslationFilter.java:116) ~[spring-security-web-5.7.7.jar:5.7.7]
		at org.springframework.security.web.FilterChainProxy$VirtualFilterChain.doFilter(FilterChainProxy.java:346) ~[spring-security-web-5.7.7.jar:5.7.7]
		at org.springframework.security.web.session.SessionManagementFilter.doFilter(SessionManagementFilter.java:126) ~[spring-security-web-5.7.7.jar:5.7.7]
		at org.springframework.security.web.session.SessionManagementFilter.doFilter(SessionManagementFilter.java:81) ~[spring-security-web-5.7.7.jar:5.7.7]
		at org.springframework.security.web.FilterChainProxy$VirtualFilterChain.doFilter(FilterChainProxy.java:346) ~[spring-security-web-5.7.7.jar:5.7.7]
		at org.springframework.security.web.authentication.AnonymousAuthenticationFilter.doFilter(AnonymousAuthenticationFilter.java:109) ~[spring-security-web-5.7.7.jar:5.7.7]
		at org.springframework.security.web.FilterChainProxy$VirtualFilterChain.doFilter(FilterChainProxy.java:346) ~[spring-security-web-5.7.7.jar:5.7.7]
		at org.springframework.security.web.servletapi.SecurityContextHolderAwareRequestFilter.doFilter(SecurityContextHolderAwareRequestFilter.java:149) ~[spring-security-web-5.7.7.jar:5.7.7]
		at org.springframework.security.web.FilterChainProxy$VirtualFilterChain.doFilter(FilterChainProxy.java:346) ~[spring-security-web-5.7.7.jar:5.7.7]
		at org.springframework.security.web.savedrequest.RequestCacheAwareFilter.doFilter(RequestCacheAwareFilter.java:63) ~[spring-security-web-5.7.7.jar:5.7.7]
		at org.springframework.security.web.FilterChainProxy$VirtualFilterChain.doFilter(FilterChainProxy.java:346) ~[spring-security-web-5.7.7.jar:5.7.7]
		at com.ktds.dsquare.auth.filter.AuthenticationAuthorizationFilter.doFilterInternal(AuthenticationAuthorizationFilter.java:63) ~[main/:na]
		at org.springframework.web.filter.OncePerRequestFilter.doFilter(OncePerRequestFilter.java:117) ~[spring-web-5.3.25.jar:5.3.25]
		at org.springframework.security.web.FilterChainProxy$VirtualFilterChain.doFilter(FilterChainProxy.java:346) ~[spring-security-web-5.7.7.jar:5.7.7]
		at org.springframework.security.web.authentication.AbstractAuthenticationProcessingFilter.doFilter(AbstractAuthenticationProcessingFilter.java:223) ~[spring-security-web-5.7.7.jar:5.7.7]
		at org.springframework.security.web.authentication.AbstractAuthenticationProcessingFilter.doFilter(AbstractAuthenticationProcessingFilter.java:217) ~[spring-security-web-5.7.7.jar:5.7.7]
		at org.springframework.security.web.FilterChainProxy$VirtualFilterChain.doFilter(FilterChainProxy.java:346) ~[spring-security-web-5.7.7.jar:5.7.7]
		at org.springframework.security.web.authentication.logout.LogoutFilter.doFilter(LogoutFilter.java:103) ~[spring-security-web-5.7.7.jar:5.7.7]
		at org.springframework.security.web.authentication.logout.LogoutFilter.doFilter(LogoutFilter.java:89) ~[spring-security-web-5.7.7.jar:5.7.7]
		at org.springframework.security.web.FilterChainProxy$VirtualFilterChain.doFilter(FilterChainProxy.java:346) ~[spring-security-web-5.7.7.jar:5.7.7]
		at org.springframework.web.filter.CorsFilter.doFilterInternal(CorsFilter.java:91) ~[spring-web-5.3.25.jar:5.3.25]
		at org.springframework.web.filter.OncePerRequestFilter.doFilter(OncePerRequestFilter.java:117) ~[spring-web-5.3.25.jar:5.3.25]
		at org.springframework.security.web.FilterChainProxy$VirtualFilterChain.doFilter(FilterChainProxy.java:346) ~[spring-security-web-5.7.7.jar:5.7.7]
		at org.springframework.security.web.header.HeaderWriterFilter.doHeadersAfter(HeaderWriterFilter.java:90) ~[spring-security-web-5.7.7.jar:5.7.7]
		at org.springframework.security.web.header.HeaderWriterFilter.doFilterInternal(HeaderWriterFilter.java:75) ~[spring-security-web-5.7.7.jar:5.7.7]
		at org.springframework.web.filter.OncePerRequestFilter.doFilter(OncePerRequestFilter.java:117) ~[spring-web-5.3.25.jar:5.3.25]
		at org.springframework.security.web.FilterChainProxy$VirtualFilterChain.doFilter(FilterChainProxy.java:346) ~[spring-security-web-5.7.7.jar:5.7.7]
		at org.springframework.security.web.context.SecurityContextPersistenceFilter.doFilter(SecurityContextPersistenceFilter.java:112) ~[spring-security-web-5.7.7.jar:5.7.7]
		at org.springframework.security.web.context.SecurityContextPersistenceFilter.doFilter(SecurityContextPersistenceFilter.java:82) ~[spring-security-web-5.7.7.jar:5.7.7]
		at org.springframework.security.web.FilterChainProxy$VirtualFilterChain.doFilter(FilterChainProxy.java:346) ~[spring-security-web-5.7.7.jar:5.7.7]
		at org.springframework.security.web.context.request.async.WebAsyncManagerIntegrationFilter.doFilterInternal(WebAsyncManagerIntegrationFilter.java:55) ~[spring-security-web-5.7.7.jar:5.7.7]
		at org.springframework.web.filter.OncePerRequestFilter.doFilter(OncePerRequestFilter.java:117) ~[spring-web-5.3.25.jar:5.3.25]
		at org.springframework.security.web.FilterChainProxy$VirtualFilterChain.doFilter(FilterChainProxy.java:346) ~[spring-security-web-5.7.7.jar:5.7.7]
		at org.springframework.security.web.session.DisableEncodeUrlFilter.doFilterInternal(DisableEncodeUrlFilter.java:42) ~[spring-security-web-5.7.7.jar:5.7.7]
		at org.springframework.web.filter.OncePerRequestFilter.doFilter(OncePerRequestFilter.java:117) ~[spring-web-5.3.25.jar:5.3.25]
		at org.springframework.security.web.FilterChainProxy$VirtualFilterChain.doFilter(FilterChainProxy.java:346) ~[spring-security-web-5.7.7.jar:5.7.7]
		at org.springframework.security.web.FilterChainProxy.doFilterInternal(FilterChainProxy.java:221) ~[spring-security-web-5.7.7.jar:5.7.7]
		at org.springframework.security.web.FilterChainProxy.doFilter(FilterChainProxy.java:186) ~[spring-security-web-5.7.7.jar:5.7.7]
		at org.springframework.web.filter.DelegatingFilterProxy.invokeDelegate(DelegatingFilterProxy.java:354) ~[spring-web-5.3.25.jar:5.3.25]
		at org.springframework.web.filter.DelegatingFilterProxy.doFilter(DelegatingFilterProxy.java:267) ~[spring-web-5.3.25.jar:5.3.25]
		at org.apache.catalina.core.ApplicationFilterChain.internalDoFilter(ApplicationFilterChain.java:189) ~[tomcat-embed-core-9.0.71.jar:9.0.71]
		at org.apache.catalina.core.ApplicationFilterChain.doFilter(ApplicationFilterChain.java:162) ~[tomcat-embed-core-9.0.71.jar:9.0.71]
		at org.springframework.web.filter.CharacterEncodingFilter.doFilterInternal(CharacterEncodingFilter.java:201) ~[spring-web-5.3.25.jar:5.3.25]
		at org.springframework.web.filter.OncePerRequestFilter.doFilter(OncePerRequestFilter.java:117) ~[spring-web-5.3.25.jar:5.3.25]
		at org.apache.catalina.core.ApplicationFilterChain.internalDoFilter(ApplicationFilterChain.java:189) ~[tomcat-embed-core-9.0.71.jar:9.0.71]
		at org.apache.catalina.core.ApplicationFilterChain.doFilter(ApplicationFilterChain.java:162) ~[tomcat-embed-core-9.0.71.jar:9.0.71]
		at org.apache.catalina.core.StandardWrapperValve.invoke(StandardWrapperValve.java:177) ~[tomcat-embed-core-9.0.71.jar:9.0.71]
		at org.apache.catalina.core.StandardContextValve.invoke(StandardContextValve.java:97) ~[tomcat-embed-core-9.0.71.jar:9.0.71]
		at org.apache.catalina.authenticator.AuthenticatorBase.invoke(AuthenticatorBase.java:541) ~[tomcat-embed-core-9.0.71.jar:9.0.71]
		at org.apache.catalina.core.StandardHostValve.invoke(StandardHostValve.java:135) ~[tomcat-embed-core-9.0.71.jar:9.0.71]
		at org.apache.catalina.valves.ErrorReportValve.invoke(ErrorReportValve.java:92) ~[tomcat-embed-core-9.0.71.jar:9.0.71]
		at org.apache.catalina.core.StandardEngineValve.invoke(StandardEngineValve.java:78) ~[tomcat-embed-core-9.0.71.jar:9.0.71]
		at org.apache.catalina.connector.CoyoteAdapter.service(CoyoteAdapter.java:360) ~[tomcat-embed-core-9.0.71.jar:9.0.71]
		at org.apache.coyote.http11.Http11Processor.service(Http11Processor.java:399) ~[tomcat-embed-core-9.0.71.jar:9.0.71]
		at org.apache.coyote.AbstractProcessorLight.process(AbstractProcessorLight.java:65) ~[tomcat-embed-core-9.0.71.jar:9.0.71]
		at org.apache.coyote.AbstractProtocol$ConnectionHandler.process(AbstractProtocol.java:891) ~[tomcat-embed-core-9.0.71.jar:9.0.71]
		at org.apache.tomcat.util.net.NioEndpoint$SocketProcessor.doRun(NioEndpoint.java:1784) ~[tomcat-embed-core-9.0.71.jar:9.0.71]
		at org.apache.tomcat.util.net.SocketProcessorBase.run(SocketProcessorBase.java:49) ~[tomcat-embed-core-9.0.71.jar:9.0.71]
		at org.apache.tomcat.util.threads.ThreadPoolExecutor.runWorker(ThreadPoolExecutor.java:1191) ~[tomcat-embed-core-9.0.71.jar:9.0.71]
		at org.apache.tomcat.util.threads.ThreadPoolExecutor$Worker.run(ThreadPoolExecutor.java:659) ~[tomcat-embed-core-9.0.71.jar:9.0.71]
		at org.apache.tomcat.util.threads.TaskThread$WrappingRunnable.run(TaskThread.java:61) ~[tomcat-embed-core-9.0.71.jar:9.0.71]
		at java.base/java.lang.Thread.run(Thread.java:833) ~[na:na]
	Caused by: org.hibernate.exception.DataException: could not execute statement
		at org.hibernate.exception.internal.SQLStateConversionDelegate.convert(SQLStateConversionDelegate.java:115) ~[hibernate-core-5.6.15.Final.jar:5.6.15.Final]
		at org.hibernate.exception.internal.StandardSQLExceptionConverter.convert(StandardSQLExceptionConverter.java:37) ~[hibernate-core-5.6.15.Final.jar:5.6.15.Final]
		at org.hibernate.engine.jdbc.spi.SqlExceptionHelper.convert(SqlExceptionHelper.java:113) ~[hibernate-core-5.6.15.Final.jar:5.6.15.Final]
		at org.hibernate.engine.jdbc.spi.SqlExceptionHelper.convert(SqlExceptionHelper.java:99) ~[hibernate-core-5.6.15.Final.jar:5.6.15.Final]
		at org.hibernate.engine.jdbc.internal.ResultSetReturnImpl.executeUpdate(ResultSetReturnImpl.java:200) ~[hibernate-core-5.6.15.Final.jar:5.6.15.Final]
		at org.hibernate.engine.jdbc.batch.internal.NonBatchingBatch.addToBatch(NonBatchingBatch.java:46) ~[hibernate-core-5.6.15.Final.jar:5.6.15.Final]
		at org.hibernate.persister.entity.AbstractEntityPersister.insert(AbstractEntityPersister.java:3375) ~[hibernate-core-5.6.15.Final.jar:5.6.15.Final]
		at org.hibernate.persister.entity.AbstractEntityPersister.insert(AbstractEntityPersister.java:3931) ~[hibernate-core-5.6.15.Final.jar:5.6.15.Final]
		at org.hibernate.action.internal.EntityInsertAction.execute(EntityInsertAction.java:107) ~[hibernate-core-5.6.15.Final.jar:5.6.15.Final]
		at org.hibernate.engine.spi.ActionQueue.executeActions(ActionQueue.java:604) ~[hibernate-core-5.6.15.Final.jar:5.6.15.Final]
		at org.hibernate.engine.spi.ActionQueue.lambda$executeActions$1(ActionQueue.java:478) ~[hibernate-core-5.6.15.Final.jar:5.6.15.Final]
		at java.base/java.util.LinkedHashMap.forEach(LinkedHashMap.java:721) ~[na:na]
		at org.hibernate.engine.spi.ActionQueue.executeActions(ActionQueue.java:475) ~[hibernate-core-5.6.15.Final.jar:5.6.15.Final]
		at org.hibernate.event.internal.AbstractFlushingEventListener.performExecutions(AbstractFlushingEventListener.java:344) ~[hibernate-core-5.6.15.Final.jar:5.6.15.Final]
		at org.hibernate.event.internal.DefaultFlushEventListener.onFlush(DefaultFlushEventListener.java:40) ~[hibernate-core-5.6.15.Final.jar:5.6.15.Final]
		at org.hibernate.event.service.internal.EventListenerGroupImpl.fireEventOnEachListener(EventListenerGroupImpl.java:107) ~[hibernate-core-5.6.15.Final.jar:5.6.15.Final]
		at org.hibernate.internal.SessionImpl.doFlush(SessionImpl.java:1407) ~[hibernate-core-5.6.15.Final.jar:5.6.15.Final]
		at org.hibernate.internal.SessionImpl.managedFlush(SessionImpl.java:489) ~[hibernate-core-5.6.15.Final.jar:5.6.15.Final]
		at org.hibernate.internal.SessionImpl.flushBeforeTransactionCompletion(SessionImpl.java:3303) ~[hibernate-core-5.6.15.Final.jar:5.6.15.Final]
		at org.hibernate.internal.SessionImpl.beforeTransactionCompletion(SessionImpl.java:2438) ~[hibernate-core-5.6.15.Final.jar:5.6.15.Final]
		at org.hibernate.engine.jdbc.internal.JdbcCoordinatorImpl.beforeTransactionCompletion(JdbcCoordinatorImpl.java:449) ~[hibernate-core-5.6.15.Final.jar:5.6.15.Final]
		at org.hibernate.resource.transaction.backend.jdbc.internal.JdbcResourceLocalTransactionCoordinatorImpl.beforeCompletionCallback(JdbcResourceLocalTransactionCoordinatorImpl.java:183) ~[hibernate-core-5.6.15.Final.jar:5.6.15.Final]
		at org.hibernate.resource.transaction.backend.jdbc.internal.JdbcResourceLocalTransactionCoordinatorImpl.access$300(JdbcResourceLocalTransactionCoordinatorImpl.java:40) ~[hibernate-core-5.6.15.Final.jar:5.6.15.Final]
		at org.hibernate.resource.transaction.backend.jdbc.internal.JdbcResourceLocalTransactionCoordinatorImpl$TransactionDriverControlImpl.commit(JdbcResourceLocalTransactionCoordinatorImpl.java:281) ~[hibernate-core-5.6.15.Final.jar:5.6.15.Final]
		at org.hibernate.engine.transaction.internal.TransactionImpl.commit(TransactionImpl.java:101) ~[hibernate-core-5.6.15.Final.jar:5.6.15.Final]
		at org.springframework.orm.jpa.JpaTransactionManager.doCommit(JpaTransactionManager.java:562) ~[spring-orm-5.3.25.jar:5.3.25]
		... 99 common frames omitted
	Caused by: org.postgresql.util.PSQLException: 오류: character varying(100) 자료형에 너무 긴 자료를 담으려고 합니다.
		at org.postgresql.core.v3.QueryExecutorImpl.receiveErrorResponse(QueryExecutorImpl.java:2675) ~[postgresql-42.3.8.jar:42.3.8]
		at org.postgresql.core.v3.QueryExecutorImpl.processResults(QueryExecutorImpl.java:2365) ~[postgresql-42.3.8.jar:42.3.8]
		at org.postgresql.core.v3.QueryExecutorImpl.execute(QueryExecutorImpl.java:355) ~[postgresql-42.3.8.jar:42.3.8]
		at org.postgresql.jdbc.PgStatement.executeInternal(PgStatement.java:490) ~[postgresql-42.3.8.jar:42.3.8]
		at org.postgresql.jdbc.PgStatement.execute(PgStatement.java:408) ~[postgresql-42.3.8.jar:42.3.8]
		at org.postgresql.jdbc.PgPreparedStatement.executeWithFlags(PgPreparedStatement.java:167) ~[postgresql-42.3.8.jar:42.3.8]
		at org.postgresql.jdbc.PgPreparedStatement.executeUpdate(PgPreparedStatement.java:135) ~[postgresql-42.3.8.jar:42.3.8]
		at com.zaxxer.hikari.pool.ProxyPreparedStatement.executeUpdate(ProxyPreparedStatement.java:61) ~[HikariCP-4.0.3.jar:na]
		at com.zaxxer.hikari.pool.HikariProxyPreparedStatement.executeUpdate(HikariProxyPreparedStatement.java) ~[HikariCP-4.0.3.jar:na]
		at org.hibernate.engine.jdbc.internal.ResultSetReturnImpl.executeUpdate(ResultSetReturnImpl.java:197) ~[hibernate-core-5.6.15.Final.jar:5.6.15.Final]
		... 120 common frames omitted


	=====================================================================

## 오류 원인
	title 컬럼에 너무긴 값 입력
	title varchar(100)
