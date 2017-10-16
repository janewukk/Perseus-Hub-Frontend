// ============= GLOBAL INITIALIZATION
// config csrf token for jQuery ajax
var csrftoken = $("[name=csrfmiddlewaretoken]").val();
function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
$.ajaxSetup({
	beforeSend: function(xhr, settings) {
		if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
			xhr.setRequestHeader("X-CSRFToken", csrftoken);
		}
	}
});

// ============== HELPER FUNCTIONS
/**
 * Requires a modal#modal element present
 * Show a modal with customized message
 * @param  {String} message Message to show
 * @return {Void}
 */
function showModal(message) {

	// set modal message
	$('#modal .modal-body').html(message);
	// show modal
	$('#modal').modal();

}

/**
 * Trigger a jquery custom event
 * @param  {jQuery.fn} $el   jQuery obj
 * @param  {String} event Name of event
 * @param  {Object} data  Data to pass into event
 * @return {Void}
 */
function trigger($el, event, data) {

	var eventData = {
		'type' : event
	}
	$el.trigger(Object.assign(eventData, data));

}

/**
 * Check if a js data type is a plain old js object
 * @param  {[type]}  obj [description]
 * @return {Boolean}     [description]
 */
function isPOJSO (obj) {

	return obj.__proto__.constructor.name == "Object";

}

/**
 * Django template utilities
 */
window.False = false;
window.True = true;

// ============== HELPER CLASSES
/**
 * A simple wrapper over the KnockoutJS MVVM
 * @param {Object} options Options to initialize
 */
window.ob = ko.observable;
window.oba = ko.observableArray;
window.obc = ko.computed;
window.obo = function(obj) {
	for (var key in obj) {
		if (obj.hasOwnProperty(key)) {
			var val = obj[key];
			if (Array.isArray(val)){
				for (var i = 0; i < val.length; ++i) {
					if (isPOJSO(val[i])) {
						obo(val[i]);
					}else {
						val[i] = ob(val[i]);
					}
				}
				obj[key] = oba(val);
			} else if (isPOJSO(val)){
				obo(val);
				obj[key] = ob(val);
			} else {
				obj[key] = ob(val);
			}
		}
	}
	return obj;

}

function View(options) {
	// init configs
	var el = null, data = {}, computed = {}, methods = {};

	// extract configurations
	if (options.el) el = options.el;
	if (options.data) data = options.data;
	if (options.computed) computed = options.computed;
	if (options.methods) methods = options.methods;
	console.log(data);
	console.log(el);

	// construct internal view model
	this.viewModel = data;
	this.constructData(this.viewModel);
	this.constructComputedData(computed);
	this.constructMethods(methods);

	// activate binding
	if (el) {
		ko.applyBindings(this.viewModel, el);
	} else {
		ko.applyBindings(this.viewModel);
	}
}

/**
 * Shortcut to retrieve the underlining view model
 * @return {Object} View model
 */
View.prototype.data = function() {
	
	return this.viewModel;

};

/**
 * Convert all input data into observables
 * @param  {Object} obj Initial data object
 * @return {Void}
 */
View.prototype.constructData = function (obj) {

	obo(obj);

}

/**
 * Make computed property functions 
 * @param  {Object} computed Computed properties function mapping
 * @return {Void}
 */
View.prototype.constructComputedData = function (computed) {
	for (var key in computed) {
		if (computed.hasOwnProperty(key)){
			this.viewModel[key] = obc(computed[key], this.viewModel)
		}
	}

}

/**
 * Make view specific methods
 * @param  {Object} methods Method function mapping
 * @return {Void}
 */
View.prototype.constructMethods = function (methods) {
	for (var key in methods) {
		if (methods.hasOwnProperty(key)) {
			this.viewModel[key] = methods[key].bind(this.viewModel);
		}
	}

}
