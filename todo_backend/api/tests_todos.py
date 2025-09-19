from rest_framework.test import APITestCase
from django.urls import reverse
from .models import ToDoItem


class ToDoCrudTests(APITestCase):
    def test_crud_flow(self):
        # Create
        create_url = reverse('todo-list-create')
        payload = {
            "title": "Test task",
            "description": "Do something",
            "is_completed": False,
            "priority": 3
        }
        res = self.client.post(create_url, payload, format='json')
        self.assertEqual(res.status_code, 201, res.data)
        item_id = res.data["id"]

        # List
        list_res = self.client.get(create_url)
        self.assertEqual(list_res.status_code, 200)
        self.assertTrue(any(x["id"] == item_id for x in list_res.data))

        # Retrieve
        detail_url = reverse('todo-detail', args=[item_id])
        get_res = self.client.get(detail_url)
        self.assertEqual(get_res.status_code, 200)
        self.assertEqual(get_res.data["title"], "Test task")

        # Patch
        patch_res = self.client.patch(detail_url, {"is_completed": True}, format='json')
        self.assertEqual(patch_res.status_code, 200)
        self.assertTrue(patch_res.data["is_completed"])

        # Put
        put_payload = {
            "title": "Updated",
            "description": "Changed",
            "is_completed": True,
            "priority": 2
        }
        put_res = self.client.put(detail_url, put_payload, format='json')
        self.assertEqual(put_res.status_code, 200)
        self.assertEqual(put_res.data["title"], "Updated")
        self.assertEqual(put_res.data["priority"], 2)

        # Delete
        del_res = self.client.delete(detail_url)
        self.assertEqual(del_res.status_code, 204)
        self.assertFalse(ToDoItem.objects.filter(id=item_id).exists())
