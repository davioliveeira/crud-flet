from flet import *
import sqlite3


class AppCrudProducts(UserControl):
    def __init__(self):
        super().__init__()

        self.all_data = Column(auto_scroll=True)
        self.add_data = TextField(label="Nome Produto")
        self.edit_data = TextField(label="Editar Produto")

        self.conn = sqlite3.connect(
            "src/db/produtos.db", check_same_thread=False)
        self.cursor = self.conn.cursor()

    def cicle(self):
        self.render_all()

    # CREATE - add new data in database
    def add_new_data(self, e):
        self.cursor.execute("INSERT INTO clientes (nome) VALUES (?)",
                            [self.add_data.value])
        self.conn.commit()

        self.all_data.controls.clear()
        self.render_all()
        self.page.update()
    # READ - Show all data in database

    def render_all(self):
        self.cursor.execute("SELECT * FROM clientes")
        self.conn.commit()

        all_datas = self.cursor.fetchall()

        for data in all_datas:
            self.all_data.controls.append(
                ListTile(subtitle=Text(data[0]),
                         title=Text(data[1]),
                         on_click=self.show_actions)
            )
        self.update()
    # UPDATE - Update data in database

    def atualization(self, nome, id_produto, alert_dialog):
        self.cursor.execute(
            "UPDATE clientes SET nome = ? WHERE id = ? ", [id_produto, nome])
        self.conn.commit()

        alert_dialog.open = False
        self.all_data.controls.clear()
        self.render_all()
        self.page.update()

    # DELETE - Delete data in database
    def delete(self, id_produto, alert_dialog):
        self.cursor.execute("DELETE FROM clientes WHERE id = ?", [id_produto])
        alert_dialog.open = False

        self.all_data.controls.clear()
        self.render_all()
        self.page.update()

    # SHOW ACTIONS

    def show_actions(self, e):
        id_produto = e.control.subtitle.value
        self.edit_data.value = e.control.title.value
        self.page.update()

        dialog_alert = AlertDialog(
            title=Text(f"Editar ID: {id_produto}"),
            content=self.edit_data,
            actions=[
                ElevatedButton("Delete", color="white",
                               bgcolor="blue",
                               on_click=lambda e: self.delete(id_produto, dialog_alert
                                                              )),
                ElevatedButton("Update", on_click=lambda e: self.atualization(
                    id_produto, self.edit_data.value, dialog_alert))
            ],
            actions_alignment='spaceBetween'
        )

        self.page.dialog = dialog_alert
        dialog_alert.open = True

        self.page.update()

    # build project
    def build(self):
        return Column([
            Text("Table Users CRUD", text_align='center', size=20, weight='bold'),
            self.add_data,
            ElevatedButton("Adicionar Produto", on_click=self.add_new_data),
            self.all_data
        ])


def main(page: Page):
    page.update()
    app_crud = AppCrudProducts()
    page.add(
        app_crud,
    )


app(main)
