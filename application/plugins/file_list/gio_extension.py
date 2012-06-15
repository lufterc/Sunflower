import gtk
import gio

from dialogs import SambaCreate, SambaResult
from plugin_base.mount_manager_extension import MountManagerExtension


class Column:
	NAME = 0
	URI = 1
	DOMAIN = 2
	REQUIRES_LOGIN = 3
	

class SambaExtension(MountManagerExtension):
	"""Mount manager extension that provides editing and mounting
	of Samba shares through GIO backend.

	"""

	def __init__(self, parent, window):
		MountManagerExtension.__init__(self, parent, window)

		# create user interface
		list_container = gtk.ScrolledWindow()
		list_container.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
		list_container.set_shadow_type(gtk.SHADOW_IN)

		self._store = gtk.ListStore(str, str, str, bool) 
		self._list = gtk.TreeView(model=self._store)

		cell_name = gtk.CellRendererText()
		cell_uri = gtk.CellRendererText()

		col_name = gtk.TreeViewColumn(_('Name'), cell_name, text=Column.NAME)
		col_uri = gtk.TreeViewColumn(_('URI'), cell_uri, text=Column.URI)

		col_name.set_expand(True)

		self._list.append_column(col_name)
		self._list.append_column(col_uri)

		# create controls
		image_add = gtk.Image()
		image_add.set_from_stock(gtk.STOCK_ADD, gtk.ICON_SIZE_BUTTON)

		button_add = gtk.Button()
		button_add.set_image(image_add)
		button_add.connect('clicked', self._add_mount)

		image_edit = gtk.Image()
		image_edit.set_from_stock(gtk.STOCK_EDIT, gtk.ICON_SIZE_BUTTON)

		button_edit = gtk.Button()
		button_edit.set_image(image_edit)
		button_edit.connect('clicked', self._edit_mount)

		image_delete = gtk.Image()
		image_delete.set_from_stock(gtk.STOCK_DELETE, gtk.ICON_SIZE_BUTTON)

		button_delete = gtk.Button()
		button_delete.set_image(image_delete)
		button_delete.connect('clicked', self._delete_mount)

		button_mount = gtk.Button(_('Mount'))
		button_mount.connect('clicked', self._mount_selected)

		button_unmount = gtk.Button(_('Unmount'))
		button_unmount.connect('clicked', self._unmount_selected)

		# pack user interface
		list_container.add(self._list)
		
		self._container.pack_start(list_container, True, True, 0)

		self._controls.pack_start(button_add, False, False, 0)
		self._controls.pack_start(button_edit, False, False, 0)
		self._controls.pack_start(button_delete, False, False, 0)
		self._controls.pack_end(button_unmount, False, False, 0)
		self._controls.pack_end(button_mount, False, False, 0)

	def __form_uri(self, params):
		"""Form URI based on result from SambaCreate dialog"""
		scheme = 'smb'
		server = params[SambaResult.SERVER]
		path = params[SambaResult.SHARE]

		# include username
		if params[SambaResult.USERNAME] != '':
			server = '{0}@{1}'.format(params[SambaResult.USERNAME], server)

		# include directory
		if params[SambaResult.DIRECTORY] != '':
			path = '{0}/{1}'.format(path, params[SambaResult.DIRECTORY])

		return '{0}://{1}/{2}/'.format(scheme, server, path)

	def _add_mount(self, widget, data=None):
		"""Present dialog to user for creating a new mount"""
		keyring_manager = self._parent._application.keyring_manager

		dialog = SambaCreate(self._window)
		dialog.set_keyring_available(keyring_manager.is_available())
		response = dialog.get_response()

		if response[0] == gtk.RESPONSE_OK:
			name = response[1][SambaResult.NAME]
			uri = self.__form_uri(response[1])
			domain = response[1][SambaResult.DOMAIN]
			requires_login = response[1][SambaResult.PASSWORD] != ''

			self._store.append((name, uri, domain, requires_login))
			keyring_manager.store_password(name, uri, response[1][SambaResult.PASSWORD])

	def _edit_mount(self, widget, data=None):
		"""Present dialog to user for editing existing mount"""
		pass

	def _delete_mount(self, widget, data=None):
		"""Remove dialog if user confirms"""
		pass

	def _mount_selected(self, widget, data=None):
		"""Mount selected item"""
		pass

	def _unmount_selected(self, widget, data=None):
		"""Unmount selected item"""
		pass

	def unmount(self, uri):
		"""Handle unmounting specified URI"""
		pass

	def get_information(self):
		"""Get extension information"""
		return 'samba', "Samba"
