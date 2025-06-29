import flet as ft
from db import main_db

def main(page: ft.Page):
    print("Starting the app...")
    page.title = "Todo App"
    # page.padding = 20
    # page.bg_color = ft.Colors.GREY_600
    page.theme_mode = ft.ThemeMode.DARK
    page.window_maximized = True

    task_list = ft.Column(spacing=10)

    filter_type = 'all'

    def load_tasks():
        task_list.controls.clear()
        for task_id, task_text, created_at, completed in main_db.get_tasks(filter_type):
            task_list.controls.append(create_task_row(task_id, task_text, created_at, completed))

        page.update() 

    def create_task_row(task_id, task_text, created_at, completed):
        task_field = ft.TextField(value=task_text, expand=True, read_only=True)

        task_checkbox = ft.Checkbox(
            value=bool(completed),
            on_change=lambda e: toggle_task(task_id, e.control.value)
        )

        created_label = ft.Text(f"Создано: {created_at}", style=ft.TextThemeStyle.BODY_SMALL, color=ft.Colors.GREY)


        def enable_edit(e):
            task_field.read_only = False
            task_field.update()

        def save_task(e):
            main_db.update_task_db(task_id, task_field.value)
            page.update()

        return ft.Row([
            task_checkbox,
            ft.Column([task_field, created_label], expand=True),
            ft.IconButton(ft.Icons.EDIT, icon_color=ft.Colors.YELLOW_400, on_click=enable_edit),
            ft.IconButton(ft.Icons.SAVE, icon_color=ft.Colors.GREEN_400, on_click=save_task),
            ft.IconButton(ft.Icons.DELETE, icon_color=ft.Colors.RED_400, on_click=lambda e: delete_task(task_id))
        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)


    def add_task(e):
        if task_input.value:
            task_id = main_db.add_task_db(task_input.value)
            task_list.controls.append(create_task_row(task_id, task_input.value, "", 0))
            task_input.value = ""
            page.update()

    def toggle_task(task_id, is_completed):
        main_db.update_task_db(task_id, completed=int(is_completed))
        load_tasks()


    def delete_task(task_id):
        main_db.delete_task_db(task_id)
        load_tasks()

    def set_filter(filter_value):
        nonlocal filter_type
        filter_type = filter_value
        load_tasks()

    def clear_completed(e):
        main_db.clear_completed_tasks()
        load_tasks()

      # Добавляем кнопку очистки
    clear_completed_button = ft.ElevatedButton(
        "Очистить выполненные",
        on_click=clear_completed,
        icon=ft.Icons.DELETE_FOREVER,
        icon_color=ft.Colors.RED_400,
        bgcolor=ft.Colors.GREY_800,
        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10))
    )

    filter_buttons = ft.Row(
        controls=[
            ft.ElevatedButton("Все", on_click=lambda e: set_filter('all')),
            ft.ElevatedButton("Завершенные", on_click=lambda e: set_filter('completed')),
            ft.ElevatedButton("Незавершенные", on_click=lambda e: set_filter('uncompleted')),
            clear_completed_button
        ],
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN
    )
    task_input = ft.TextField(hint_text="Добавьте задачу: ", expand=True, dense=True, on_submit=add_task)

    add_button = ft.ElevatedButton("Добавить", on_click=add_task, icon=ft.Icons.ADD, icon_color=ft.Colors.GREEN_400)

    # page.add(ft.Column({
    #     ft.Row({task_input, add_button}, alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
    #     task_list
    # }))

    content = ft.Container(
        content=ft.Column(
            controls=[
                ft.Row(
                    controls=[task_input, add_button],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                ),
                filter_buttons,
                task_list
            ],
            alignment=ft.MainAxisAlignment.CENTER
        ),
        padding=20,
        alignment=ft.alignment.center
    )

    background_image = ft.Image(
        src="media/thumb-1920-1015665.png",
        fit=ft.ImageFit.FILL,
        width=page.width,
        height=page.height
    )   

    background = ft.Stack(controls=[background_image, content])

    def on_resize(e):
        background_image.width = page.width
        background_image.height = page.height
        background.update()

    page.add(background)
    page.on_resize = on_resize

    load_tasks()

if __name__ == "__main__":
    main_db.init_db()
    ft.app(target=main)