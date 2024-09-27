from django.apps import AppConfig
from django.db.utils import OperationalError

class ClothesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'clothes'

    def ready(self):
        """
        プロジェクトが開始されるたびに Site のデータを自動的に更新または作成する
        """
        from django.contrib.sites.models import Site
        try:
            Site.objects.update_or_create(
                id=1,  # 更新または作成したいSiteのID
                defaults={
                    "domain": "127.0.0.1:8000",
                    "name": "Localhost"
                }
            )
        except OperationalError:
            # データベースがまだ作成されていない場合
            pass
