// ============= GLOBAL INITIALIZATION
// config csrf token for jQuery ajax
var csrftoken = Cookies.get('csrftoken');
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
// config csrf token for Axios
axios.defaults.headers.common['X-CSRFToken'] = csrftoken;
window.http = axios;

// ============== HELPER FUNCTIONS
/**
 * Requires a modal#modal element present
 * Show a modal with customized message
 * @param  {String} message Message to show
 * @return {Void}
 */
function showModal(message) {
	// set error message
	$('#modal .modal-body').html(message);
	// show modal
	$('#modal').modal();
}

// ============== HELPER CLASSES
/**
 * A simple wrapper over the KnockoutJS MVVM
 * @param {Object} options Options to initialize
 */
function View(options) {
	// init configs
	var el = null, data = {}, computed = {};

	// extract configurations
	if (options.el) el = options.el;
	if (options.data) data = options.data;
	if (options.computed) computed = options.computed;

	// construct internal view model
	this.viewModel = data;

	this.constructModel(this.viewModel);

	for (var key in computed) {
		this.viewModel[key] = ko.computed(computed[key], this.viewModel)
	}

	// activate binding
	if (el) {
		ko.applyBindings(this.viewModel, el)
	} else {
		ko.applyBindings(this.viewModel)
	}
}

View.prototype.constructModel = function (obj) {
	var key, has = Object.prototype.hasOwnProperty.bind(obj);
	for (key in obj) {
		if (has(key)) {
			var val = obj[key];
			if (Array.isArray(val)){
				for (var i = 0; i < val.length; ++i) {
					this.constructModel(val[i]);
				}
				obj[key] = ko.observableArray(val);
			} else {
				obj[key] = ko.observable(val);
			}
		}
	}
}

/**
 * Subscribe to changes of a view data
 * @param  {String}   key      Name of data
 * @param  {Function} callback<newValue>
 * @return {Void}
 */
View.prototype.subscribe = function(key, callback) {

	this.viewModel[key].subscribe(callback);

}

/**
 * Shortcut to retrieve the underlining view model
 * @return {Object} View model
 */
View.prototype.data = function() {
	
	return this.viewModel;

};
