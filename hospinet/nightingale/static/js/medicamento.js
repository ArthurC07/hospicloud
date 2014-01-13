function Medicamento(url, target) {
	this.url = url;
	this.location = target;
}

Medicamento.prototype.notificar = function() {
	var base_url = this.url;
	var location = this.location;
	var destination = this.location;
	var now = new Date();
	var proximo = new Date(now.getTime() + 20*60000);
	$.get(base_url + 'api/mobile/medicamento/?proxima_dosis__lte=' + proximo.toISOString(), function(data) {
		$.each(data.objects, function(i, medicamento) {
			$.pnotify({
				title: 'Suministrar Medicamento',
				text: '<a href="' + location + medicamento.id + '/dosificar">' + medicamento.cargo.descripcion + ' a ' +
				medicamento.admision.paciente.nombre + ' ' + medicamento.admision.paciente.apellido + '</a>',
				hide: false
			});
		});
	});
}
