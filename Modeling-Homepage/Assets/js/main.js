$(function(){
	var w_w=$(window).width();
	var m_l=(1920-w_w)/2;
	$('.fw .fw_bg img').css('margin-left','-'+m_l+'px');
	$('.join .bg img').css('margin-left','-'+m_l+'px');
	$('.banner_s img').css('margin-left','-'+m_l+'px');
	
	$('.nav_m .n_icon').click(function(){
		$(this).siblings('ul').slideToggle();
	});
	$('.nav_m ul li').click(function(){
		$(this).parents('ul').slideUp();	
	});
	
	$('.solution li:last-child').css('margin-right',0+'px');
	$('.pro_l li:last-child').css('margin-right',0+'px');
	
	var srw=$('.scd').width();
	var s_lw=$('.scd_l').width()+45;
	$('.scd .scd_r').width(srw-s_lw+'px');
	var slh=$('.scd .scd_r').height();
	$('.scd .scd_l').height(slh+'px');
	
	$('.contact_m ul li:last-child').css('margin-right',0+'px');
	
})